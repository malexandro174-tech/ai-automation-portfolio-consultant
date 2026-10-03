"""Generation through a configured compatible Broker, never a raw provider key."""
import json,os,threading,urllib.error
from .embeddings import RagError,bounded_request
class ScopedGenerator:
    def __init__(self):self.calls=0;self.local=threading.local()
    def thread_calls(self):return getattr(self.local,'calls',0)
    def generate(self,question,chunks,mode,timeout=20,validation_retry=False):
        self.calls+=1;self.local.calls=getattr(self.local,'calls',0)+1
        from .config import BASE
        payload={'requester_id':os.environ['RAG_BROKER_REQUESTER'],'capability':'CHAT_COMPLETION','payload':{'model':'deepseek-chat','messages':[{'role':'system','content':(BASE/'prompts/system_v2.txt').read_text()}, {'role':'user','content':json.dumps({'question':question,'mode':mode,'APPROVED_CONTEXT':[{k:c[k] for k in ('chunk_id','doc_id','title','category','case_id','text')} for c in chunks]},ensure_ascii=False)}],'temperature':0,'max_tokens':1000}}
        if validation_retry:
            payload['payload']['messages'].append({'role':'user','content':'Предыдущий ответ не прошёл проверку источников. Верни только точные непрерывные цитаты из text без заголовков, с chunk_id текущего контекста. Для matcher каждый case_id должен иметь собственную цитату. Если это невозможно, верни fallback:true.'})
        try:
            response=bounded_request(os.environ['RAG_BROKER_URL'].rstrip('/')+'/deepseek/complete',payload,timeout=min(20,timeout),limit=98304)
            raw=response['choices'][0]['message']['content'].strip()
            if raw.startswith('```'):
                import re
                raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw)
            usage=response.get('usage',{});usage['model']=response.get('model')
            return json.loads(raw),usage
        except urllib.error.HTTPError as e:raise RagError('BROKER_POLICY_DENIED' if e.code==403 else 'LLM_UNAVAILABLE') from e
        except (OSError,ValueError,KeyError,IndexError) as e:raise RagError('LLM_UNAVAILABLE') from e
