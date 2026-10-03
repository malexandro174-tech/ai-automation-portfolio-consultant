"""Fixed RAG parameters; deployment connections are configured separately."""
from pathlib import Path
BASE=Path(__file__).resolve().parent
DEFAULTS={'threshold':.50,'candidate_k':12,'final_k':4,'matcher_k':6,'rrf_k':60,
          'session_ttl':1800,'max_sessions':512,'memory_entries':6,
          'deadline_seconds':24,'max_context_tokens':2200,'retrieval_mode':'hybrid'}
def settings():return dict(DEFAULTS)
