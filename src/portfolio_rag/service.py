import hashlib,json,re,time,uuid
from psycopg.types.json import Jsonb
import psycopg
from .config import settings
from .db import connect
from .embeddings import RagError,token_count
from .generation import validate_generated
from .knowledge import scan
from .memory import Memory
from .retrieval import Retriever,normalize

UNKNOWN='В моей базе знаний нет подтверждённой информации по этому вопросу.'
ATTACK=re.compile(r'(?i)ignore.*instructions|reveal.*(?:prompt|secret)|show.*(?:api.?key|password)|use hidden configuration|send lead automatically|игнорир|раскрой.*(?:промпт|ключ|секрет)|покажи.*(?:ключ|парол)|отправ.*(?:автоматич|без.*подтвержд)|выполни.*команд')
COMMERCIAL=re.compile(r'(?i)заказ|обсуд|заявк|стоим|цен|автоматиз|хотим|нужен')
UNSUPPORTED=re.compile(r'(?i)\bSAP\b|биткоин|bitcoin|2035|секретный клиент|точн.*(?:цен|стоим|срок)|гаранти.*(?:продаж|срок|рост)')

class RagService:
    def __init__(self,embeddings,generator):
        self.embeddings=embeddings;self.generator=generator;self.retriever=Retriever(embeddings)
        cfg=settings();self.memory=Memory(cfg['session_ttl'],cfg['max_sessions'],cfg['memory_entries'])
    def query(self,session_id,message,mode='auto'):
        started=time.perf_counter();cid=uuid.uuid4().hex;events=[];timings={};retrieved_count=0;embedding_before,cache_before=self.embeddings.thread_counts();llm_before=self.generator.thread_calls() if hasattr(self.generator,'thread_calls') else self.generator.calls
        def event(name,**metadata):events.append((name,metadata))
        event('rag.query_received',mode=mode)
        result={'answer':UNKNOWN,'sources':[],'matched_cases':[],'fallback':True,'fallback_reason':'RETRIEVAL_EMPTY',
          'processing_ms':0,'retrieval_ms':0,'llm_ms':0,'correlation_id':cid,'mode':mode,'lead_handoff':False,'auto_send':False,
          'problem_summary':None,'relevant_capabilities':[],'suggested_direction':None,'missing_information':[],'follow_up_questions':[]}
        try:
            if not re.fullmatch(r'[A-Za-z0-9_-]{12,96}',session_id) or not 2<=len(message.strip())<=1200 or mode not in ('qa','solution_matcher','auto'):raise RagError('INVALID_REQUEST')
            if ATTACK.search(message) or any(scan(message).values()):raise RagError('POLICY_DENIED')
            if UNSUPPORTED.search(message):raise RagError('NO_CONFIDENT_MATCH' if mode=='solution_matcher' else 'OUT_OF_SCOPE')
            normalized=normalize(message,self.memory.previous(session_id));timings['query_normalize_ms']=round((time.perf_counter()-started)*1000,3)
            handoff_intent=bool(re.search(r'(?i)как.*(?:заявк|связаться)|оставить.*заявк|как.*контакт',message))
            resolved='solution_matcher' if mode=='solution_matcher' or (mode=='auto' and not handoff_intent and re.search(r'(?i)похож|подход.*кейс|хотим|нужен|подходит.*опыт|теряем|теряются',message)) else 'qa'
            result['mode']=resolved
            retrieved=self.retriever.search(normalized['normalized'],matcher=resolved=='solution_matcher')
            retrieved_count=len(retrieved['chunks'])
            timings.update(retrieved['timings']);result['retrieval_ms']=round(sum(retrieved['timings'].values()),3)
            event('rag.embedding_completed',duration_ms=timings['embedding_ms'],dimension=1024)
            event('rag.retrieval_completed',count=len(retrieved['candidates']),vector_ms=timings['vector_ms'],lexical_ms=timings['lexical_ms'])
            event('rag.fusion_completed',retrieved_count=len(retrieved['chunks']),context_token_estimate=retrieved['context_token_estimate'])
            if not retrieved['chunks']:raise RagError('NO_CONFIDENT_MATCH' if resolved=='solution_matcher' else 'RETRIEVAL_EMPTY')
            remaining=settings()['deadline_seconds']-(time.perf_counter()-started)
            if remaining<=1:raise RagError('TIMEOUT')
            t=time.perf_counter()
            for attempt in range(3):
                remaining=settings()['deadline_seconds']-(time.perf_counter()-started)
                try:
                    raw,usage=self.generator.generate(normalized['normalized'],retrieved['chunks'],resolved,timeout=remaining)
                    break
                except RagError as err:
                    remaining=settings()['deadline_seconds']-(time.perf_counter()-started)
                    if err.code!='LLM_UNAVAILABLE' or attempt==2 or remaining<5:raise
                    event('rag.llm_retry',attempt=attempt+1,reason=err.code)
                    time.sleep(.2)
            try:valid=validate_generated(raw,retrieved['chunks'],resolved)
            except RagError as err:
                remaining=settings()['deadline_seconds']-(time.perf_counter()-started)
                if err.code!='SOURCE_VALIDATION_FAILED' or remaining<5:raise
                # A bounded repair generation never weakens exact citation checks.
                event('rag.source_validation_failed',reason=err.code,retry=True)
                previous_usage=usage
                raw,usage=self.generator.generate(normalized['normalized'],retrieved['chunks'],resolved,timeout=remaining,validation_retry=True)
                usage={k:previous_usage.get(k,0)+usage.get(k,0) for k in ('prompt_tokens','completion_tokens')}
                valid=validate_generated(raw,retrieved['chunks'],resolved)
            timings['llm_ms']=round((time.perf_counter()-t)*1000,3);result['llm_ms']=timings['llm_ms']
            event('rag.llm_completed',duration_ms=timings['llm_ms'],input_tokens=usage.get('prompt_tokens'),output_tokens=usage.get('completion_tokens'))
            if valid['fallback']:raise RagError('NO_CONFIDENT_MATCH' if resolved=='solution_matcher' else 'RETRIEVAL_EMPTY')
            catalog={r['chunk_id']:r for r in retrieved['chunks']};sources={}
            for fact in valid['facts']:
                r=catalog[fact['chunk_id']];sources[r['chunk_id']]={'title':r['title'],'document_id':r['doc_id'],'source_url':r['source_url'],'section':r['section'],'score':round(r['score'],5),'chunk_id':r['chunk_id'],'version':r['document_version']}
            result.update(answer='\n\n'.join(f['quote'] for f in valid['facts']),sources=list(sources.values()),fallback=False,fallback_reason=None)
            if resolved=='solution_matcher':
                for case_id in valid['matched_cases']:
                    facts=[f for f in valid['facts'] if catalog[f['chunk_id']]['case_id']==case_id]
                    r=catalog[facts[0]['chunk_id']]
                    result['matched_cases'].append({'case_id':case_id,'title':r['title'],'why_relevant':' '.join(f['quote'] for f in facts),'source_ids':[f['chunk_id'] for f in facts]})
                result['problem_summary']=message[:300]
                result['relevant_capabilities']=[f['quote'] for f in valid['facts']]
                result['suggested_direction']='Предложение для обсуждения: уточнить входные данные и ограничения, затем проверить прототип на основе подхода выбранных кейсов. Это не утверждение о готовой интеграции для вашей задачи.'
                result['follow_up_questions']=valid['questions'] or ['Какие данные поступают на вход?','Каким должен быть результат?','Какие ограничения доступа и размещения важны?']
                result['missing_information']=result['follow_up_questions'];event('rag.solution_matcher',case_count=len(result['matched_cases']))
            result['lead_handoff']=bool(COMMERCIAL.search(message))
            if result['lead_handoff']:event('rag.lead_cta',auto_send=False)
            self.memory.add(session_id,'user',normalized['original']);self.memory.add(session_id,'assistant',result['answer'])
            result['usage']={'input_tokens':usage.get('prompt_tokens'),'output_tokens':usage.get('completion_tokens'),'cache_hit_tokens':usage.get('prompt_cache_hit_tokens',0),'cache_miss_tokens':usage.get('prompt_cache_miss_tokens',usage.get('prompt_tokens',0)),'model':usage.get('model')}
        except RagError as e:
            result['fallback_reason']=e.code
            if e.code=='NO_CONFIDENT_MATCH':
                result['problem_summary']=message[:300]
                result['missing_information']=['Нет подтверждённого похожего кейса; нужны входные данные, ожидаемый результат и ограничения.']
                result['follow_up_questions']=['Какие данные и системы участвуют в задаче?','Какой результат нужен?']
            event('rag.source_validation_failed' if e.code=='SOURCE_VALIDATION_FAILED' else 'rag.fallback',reason=e.code)
        except psycopg.Error:
            result['fallback_reason']='VECTOR_DB_UNAVAILABLE';event('rag.failed',code='VECTOR_DB_UNAVAILABLE')
        except Exception:
            result['fallback_reason']='INTERNAL_ERROR';event('rag.failed',code='INTERNAL_ERROR')
        result['processing_ms']=round((time.perf_counter()-started)*1000,3);timings['total_ms']=result['processing_ms'];result['timings']=timings
        embedding_after,cache_after=self.embeddings.thread_counts();llm_after=self.generator.thread_calls() if hasattr(self.generator,'thread_calls') else self.generator.calls
        result['cost_metadata']={'embedding_calls':embedding_after-embedding_before,'llm_calls':llm_after-llm_before,'retrieved_chunks':retrieved_count,'cited_chunks':len(result['sources']),'cache_hit':cache_after>cache_before,'currency':None,'monetary_cost':None}
        try:
            with connect() as c:
                for name,meta in events:c.execute('INSERT INTO portfolio_rag.retrieval_events(correlation_id,event,metadata) VALUES(%s,%s,%s)',(cid,name,Jsonb(meta)))
                c.execute('INSERT INTO portfolio_rag.rag_queries(correlation_id,session_hash,mode,fallback,metrics) VALUES(%s,%s,%s,%s,%s)',(cid,hashlib.sha256(session_id.encode()).hexdigest()[:16],mode,result['fallback'],Jsonb({'timings':timings,'cost_metadata':result['cost_metadata'],'usage':result.get('usage')})))
        except psycopg.Error:result['telemetry_degraded']=True
        return result
