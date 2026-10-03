import json,re,time
from .db import connect
from .embeddings import RagError
from .config import settings

def normalize(query,previous=''):
    q=' '.join(re.sub(r'[\x00-\x1f\x7f]',' ',query).split())
    follow=bool(re.match(r'(?i)^(а\s|какие результаты|что он|как он|а где|можно ли его)',q))
    normalized=q+(' '+previous if previous and follow else '')
    return {'original':q,'normalized':normalized[:1800],'followup':follow,
            'technologies':re.findall(r'(?i)\b(?:n8n|AssemblyAI|PostgreSQL|DeepSeek|Telegram|RAG|Docker|NocoDB)\b',q)}

class Retriever:
    def __init__(self,embeddings):self.embeddings=embeddings
    def search(self,query,mode=None,matcher=False,threshold=None):
        cfg=settings();mode=mode or cfg['retrieval_mode'];threshold=cfg['threshold'] if threshold is None else threshold
        timings={};start=time.perf_counter();vec=self.embeddings.embed(query)
        timings['embedding_ms']=round((time.perf_counter()-start)*1000,3)
        with connect(True) as c:
            if c.execute('SELECT count(*) AS n FROM portfolio_rag.active_chunks WHERE model_revision<>%s',(self.embeddings.revision,)).fetchone()['n']:
                raise RagError('EMBEDDING_MODEL_MISMATCH')
            start=time.perf_counter()
            vectors=c.execute('SELECT chunk_id,doc_id,document_version,title,section,category,text,source_url,tags,case_id,token_count,1-(embedding <=> %s::vector) AS similarity FROM portfolio_rag.active_chunks WHERE (%s=false OR category=%s) ORDER BY embedding <=> %s::vector LIMIT %s',(json.dumps(vec),matcher,'portfolio',json.dumps(vec),cfg['candidate_k'])).fetchall()
            timings['vector_ms']=round((time.perf_counter()-start)*1000,3)
            start=time.perf_counter()
            terms=re.findall(r'[a-zа-яё0-9]{3,}',query.lower())
            stop={'как','какие','какой','что','где','есть','для','используется','устроен','расскажите','работают','делает','умеет','возможности','подтверждён','опыт'}
            lex_query=' OR '.join(t for t in terms if t not in stop) or query
            lexical=c.execute("SELECT chunk_id,doc_id,document_version,title,section,category,text,source_url,tags,case_id,token_count,ts_rank_cd(setweight(to_tsvector('simple',title),'A')||search_tsv,websearch_to_tsquery('russian',%s)||websearch_to_tsquery('simple',%s)) AS lexical_score FROM portfolio_rag.active_chunks WHERE (%s=false OR category=%s) AND search_tsv @@ (websearch_to_tsquery('russian',%s)||websearch_to_tsquery('simple',%s)) ORDER BY lexical_score DESC,doc_id LIMIT %s",(lex_query,lex_query,matcher,'portfolio',lex_query,lex_query,cfg['candidate_k'])).fetchall()
            timings['lexical_ms']=round((time.perf_counter()-start)*1000,3)
        start=time.perf_counter();pool={};ranks={};cos={r['chunk_id']:float(r['similarity']) for r in vectors}
        for family,rows in [('vector',vectors),('lexical',lexical)]:
            for rank,row in enumerate(rows,1):
                if family=='vector' and float(row['similarity'])<threshold:continue
                cid=row['chunk_id'];pool[cid]={**pool.get(cid,{}),**row};ranks.setdefault(cid,{})[family]=rank
        if mode=='vector':allowed=[r['chunk_id'] for r in vectors if r['similarity']>=threshold]
        elif mode=='lexical':allowed=[r['chunk_id'] for r in lexical]
        else:allowed=list(pool)
        result=[]
        for cid in allowed:
            row=pool[cid];rr=ranks[cid]
            row['score']=cos.get(cid,0.0)
            row['rrf']=sum(1/(cfg['rrf_k']+r) for r in rr.values())
            # Exact project/title terms: bounded tie-break, not evidence creation.
            words=set(re.findall(r'[a-z0-9]{3,}',query.lower()))
            title=set(re.findall(r'[a-z0-9]{3,}',row['title'].lower()))
            row['metadata_boost']=min(.004,.001*len(words&title))
            row['fusion_score']=row['rrf']+row['metadata_boost']
            result.append(row)
        if mode=='vector':result.sort(key=lambda r:(r['score'],r['doc_id']),reverse=True)
        elif mode=='lexical':result.sort(key=lambda r:(r.get('lexical_score',0),r['metadata_boost']),reverse=True)
        else:result.sort(key=lambda r:(r['fusion_score'],r['score']),reverse=True)
        candidates=result[:cfg['candidate_k']];final=[];cases=set();context=0
        for row in candidates:
            if matcher and row['case_id'] not in cases and len(cases)>=3:continue
            if context+row['token_count']>cfg['max_context_tokens']:continue
            if matcher:cases.add(row['case_id'])
            final.append(row);context+=row['token_count']
            if len(final)>=(cfg['matcher_k'] if matcher else cfg['final_k']):break
        timings['fusion_ms']=round((time.perf_counter()-start)*1000,3)
        return {'candidates':candidates,'chunks':final,'timings':timings,'context_token_estimate':context,'mode':mode}
