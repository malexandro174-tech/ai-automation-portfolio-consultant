import re
from urllib.parse import urlparse
ALLOWED_HOSTS={'github.com','raw.githubusercontent.com','ai.mag-astro.ru','huggingface.co','bge-model.com','www.postgresql.org','docs.n8n.io'}
SECRET=re.compile(r'(?i)(?:sk-[a-z0-9_-]{18,}|-----BEGIN .*PRIVATE KEY|(?:password|api_key|token|secret)\s*[:=]\s*["\']?[a-z0-9_-]{16,}|postgres(?:ql)?://[^\s]+:[^\s]+@)')
PRIVATE=re.compile(r'(?i)(?:[A-Z]:\\|/opt/|/root/|/run/secrets|\b10\.\d+\.\d+\.\d+\b|\b192\.168\.\d+\.\d+\b|\b172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+\b)')
PII=re.compile(r'(?i)(?:\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b|\+7[\s()-]*\d(?:[\s()-]*\d){9}\b)')
INSTRUCTIONS=re.compile(r'(?i)ignore (?:all |previous )?instructions|reveal system prompt|show api key|use hidden configuration|send lead automatically|игнорируй.*инструкц|раскрой.*(?:ключ|промпт)')

def safe_url(url):
    if url is None:return True
    p=urlparse(url)
    return p.scheme=='https' and p.hostname in ALLOWED_HOSTS and not p.username and not p.password

def scan(text):
    return {'secret':bool(SECRET.search(text)),'private_path_or_ip':bool(PRIVATE.search(text)), 'pii':bool(PII.search(text)),'instruction':bool(INSTRUCTIONS.search(text))}

