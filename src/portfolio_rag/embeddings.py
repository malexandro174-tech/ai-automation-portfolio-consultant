import hashlib,json,math,os,threading,time,urllib.request,urllib.error

class RagError(Exception):
    def __init__(self,code):self.code=code;super().__init__(code)

def token_count(text):
    raise RagError('LOCAL_TOKENIZER_NOT_AVAILABLE')

def bounded_request(url,payload=None,timeout=10,limit=262144):
    req=urllib.request.Request(url,data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='GET' if payload is None else 'POST')
    with urllib.request.urlopen(req,timeout=timeout) as response:
        raw=response.read(limit+1)
        if len(raw)>limit:raise RagError('UPSTREAM_RESPONSE_TOO_LARGE')
        return json.loads(raw)

class Embeddings:
    def __init__(self):
        self.endpoint=os.environ['RAG_TEI_URL'].rstrip('/')
        self.info=bounded_request(self.endpoint+'/info')
        if self.info['model_id']!='BAAI/bge-m3' or self.info['max_input_length']!=512:raise RagError('EMBEDDING_MODEL_MISMATCH')
        # The immutable model fingerprint is checked before retrieval.
        self.revision=hashlib.sha256(json.dumps(self.info,sort_keys=True).encode()).hexdigest()[:20]
        from pathlib import Path
        pin=Path(__file__).with_name('model_pin.json')
        if pin.exists() and json.loads(pin.read_text())['info_fingerprint']!=self.revision:raise RagError('EMBEDDING_MODEL_MISMATCH')
        self.calls=0;self.cache_hits=0;self.local=threading.local();self.lock=threading.Lock()
    def thread_counts(self):return getattr(self.local,'calls',0),0
    def embed(self,text,use_cache=False):
        if not 1<=len(text)<=1800:raise RagError('EMBEDDING_INPUT_TOO_LONG')
        started=time.perf_counter()
        try:
            with self.lock:
                self.calls+=1;self.local.calls=getattr(self.local,'calls',0)+1
                # Existing TEI enforces exact 512-token bound and rejects oversize input; never silently truncate.
                result=bounded_request(self.endpoint+'/embed',{'inputs':[text],'truncate':False},timeout=10)
            vec=result[0]
            if len(vec)!=1024 or not all(math.isfinite(x) for x in vec):raise RagError('EMBEDDING_DIMENSION_MISMATCH')
        except urllib.error.HTTPError as e:
            raise RagError('EMBEDDING_INPUT_TOO_LONG' if e.code in (400,413,422) else 'EMBEDDING_UNAVAILABLE') from e
        except (OSError,ValueError,KeyError,IndexError) as e:raise RagError('EMBEDDING_UNAVAILABLE') from e
        self.last_ms=round((time.perf_counter()-started)*1000,3);return vec
