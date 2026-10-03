"""Public API integration surface; private admission endpoints are excluded."""
import asyncio,hashlib,json,os,re,time
from collections import OrderedDict,deque
from pathlib import Path
from fastapi import Request
from fastapi.responses import JSONResponse,HTMLResponse

def install_public(app,service,slot):
    buckets=OrderedDict()
    root=Path(__file__).parent/'knowledge_public'
    async def parse(request):
        if request.headers.get('origin') not in (None,os.environ.get('RAG_PUBLIC_ORIGIN','https://ai.mag-astro.ru')):return None,JSONResponse({'error':'ORIGIN_NOT_ALLOWED'},status_code=403)
        raw=await request.body()
        if len(raw)>4096:return None,JSONResponse({'error':'BODY_TOO_LARGE'},status_code=413)
        key=hashlib.sha256(request.headers.get('x-real-ip',request.client.host).encode()).hexdigest()[:24]
        now=time.monotonic();b=buckets.setdefault(key,deque());buckets.move_to_end(key)
        while b and now-b[0]>=600:b.popleft()
        while len(buckets)>512:buckets.popitem(last=False)
        if len(b)>=20:return None,JSONResponse({'error':'RATE_LIMITED'},status_code=429,headers={'Retry-After':'600'})
        b.append(now)
        try:d=json.loads(raw)
        except ValueError:return None,JSONResponse({'error':'INVALID_JSON'},status_code=400)
        if not isinstance(d,dict) or not isinstance(d.get('session_id'),str) or not re.fullmatch(r'[A-Za-z0-9_-]{12,96}',d['session_id']):return None,JSONResponse({'error':'INVALID_SESSION'},status_code=400)
        return d,None

    @app.post('/api/v2/portfolio-consultant/chat',include_in_schema=False)
    async def chat(request:Request):
        data,error=await parse(request)
        if error is not None:return error
        msg=data.get('message');mode=data.get('mode','auto')
        if not isinstance(msg,str) or not 2<=len(msg.strip())<=1200 or mode not in ('qa','auto','solution_matcher'):return JSONResponse({'error':'INVALID_REQUEST'},status_code=400)
        try:await asyncio.wait_for(slot.acquire(),timeout=.25)
        except asyncio.TimeoutError:return JSONResponse({'error':'BUSY'},status_code=429,headers={'Retry-After':'3'})
        try:
            # The generator and DB have their own bounded timeouts. Hold the slot until the
            # worker finishes, even if the visitor disconnects, to prevent parallel peaks.
            job=asyncio.create_task(asyncio.to_thread(service.query,data['session_id'],msg.strip(),mode))
            try:result=await asyncio.shield(job)
            except asyncio.CancelledError:
                await job
                raise
            return JSONResponse({'success':True,'provider':'grounded-rag-v2',**result},headers={'Cache-Control':'no-store'})
        finally:slot.release()

    @app.post('/api/v2/portfolio-consultant/session/clear',include_in_schema=False)
    async def clear(request:Request):
        data,error=await parse(request)
        if error is not None:return error
        with service.memory.lock:service.memory.data.pop(data['session_id'],None)
        return JSONResponse({'success':True},headers={'Cache-Control':'no-store'})

    @app.get('/knowledge/{slug}',include_in_schema=False)
    async def knowledge(slug:str):
        if not re.fullmatch(r'[a-z0-9-]{3,80}',slug):return HTMLResponse('Not found',status_code=404)
        p=root/(slug+'.html')
        if not p.is_file() or p.is_symlink():return HTMLResponse('Not found',status_code=404)
        return HTMLResponse(p.read_text(encoding='utf-8'),headers={'Cache-Control':'public, max-age=300'})
