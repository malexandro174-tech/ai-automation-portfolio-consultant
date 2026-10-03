"""Separate reader and anonymous-telemetry connections; no admin access."""
import os
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
def connect(readonly=False):
    prefix='RAG_READER' if readonly else 'RAG_TELEMETRY'
    secret=Path(os.environ[prefix+'_PASSWORD_FILE'])
    return psycopg.connect(host=os.environ['RAG_DB_HOST'],port=int(os.environ.get('RAG_DB_PORT','5432')),
      dbname=os.environ['RAG_DB_NAME'],user=os.environ[prefix+'_USER'],password=secret.read_text().strip(),
      connect_timeout=2,row_factory=dict_row,options='-c statement_timeout=3000 -c lock_timeout=2000')
