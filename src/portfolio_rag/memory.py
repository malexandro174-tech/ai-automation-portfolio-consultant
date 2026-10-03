from collections import OrderedDict,deque
import threading,time

class Memory:
    def __init__(self,ttl=1800,max_sessions=512,entries=6,clock=time.monotonic):
        self.ttl=ttl;self.max_sessions=max_sessions;self.entries=entries;self.clock=clock
        self.data=OrderedDict();self.lock=threading.RLock()
    def _expire(self):
        now=self.clock()
        for sid in list(self.data):
            if now-self.data[sid]['time']>=self.ttl:del self.data[sid]
    def previous(self,sid):
        with self.lock:
            self._expire();s=self.data.get(sid)
            if not s:return ''
            s['time']=self.clock();self.data.move_to_end(sid)
            return next((text for role,text in reversed(s['items']) if role=='user'),'')
    def add(self,sid,role,text):
        with self.lock:
            self._expire()
            if sid not in self.data:
                if len(self.data)>=self.max_sessions:self.data.popitem(last=False)
                self.data[sid]={'time':self.clock(),'items':deque(maxlen=self.entries)}
            self.data[sid]['items'].append((role,text[:800]));self.data[sid]['time']=self.clock()
    def clear(self,sid):
        with self.lock:self.data.pop(sid,None)
