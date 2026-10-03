from .embeddings import RagError
from .knowledge import scan,safe_url
def validate_generated(data,chunks,mode):
    if not isinstance(data,dict) or type(data.get('fallback')) is not bool:raise RagError('SOURCE_VALIDATION_FAILED')
    if data['fallback']:return {'fallback':True,'facts':[],'matched_cases':[],'questions':[]}
    facts=data.get('facts');matched=data.get('matched_cases',[]);questions=data.get('questions',[])
    if not isinstance(facts,list) or not 1<=len(facts)<=4 or not isinstance(matched,list) or len(set(matched))!=len(matched) or len(matched)>3:raise RagError('SOURCE_VALIDATION_FAILED')
    if not isinstance(questions,list) or len(questions)>3 or any(not isinstance(q,str) or len(q)>200 or any(scan(q).values()) for q in questions):raise RagError('SOURCE_VALIDATION_FAILED')
    catalog={r['chunk_id']:r for r in chunks};used=[]
    for fact in facts:
        if not isinstance(fact,dict) or fact.get('chunk_id') not in catalog:raise RagError('SOURCE_VALIDATION_FAILED')
        quote=fact.get('quote');row=catalog[fact['chunk_id']]
        if not isinstance(quote,str) or not 15<=len(quote)<=600 or quote not in row['text'] or any(scan(quote).values()) or not safe_url(row['source_url']):raise RagError('SOURCE_VALIDATION_FAILED')
        if quote.startswith('##') or '\n##' in quote:raise RagError('SOURCE_VALIDATION_FAILED')
        used.append(row)
    if mode=='solution_matcher':
        if not matched or any(cid not in {r['case_id'] for r in used if r['category']=='portfolio'} for cid in matched):raise RagError('SOURCE_VALIDATION_FAILED')
    elif matched:raise RagError('SOURCE_VALIDATION_FAILED')
    return {'fallback':False,'facts':facts,'matched_cases':matched,'questions':questions}
