CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS portfolio_rag;
CREATE TABLE IF NOT EXISTS portfolio_rag.documents (
 doc_id text PRIMARY KEY, title text NOT NULL, category text NOT NULL,
 source_url text, case_id text, status text NOT NULL CHECK(status IN ('ACTIVE','DEPRECATED','REMOVED')),
 public_safe boolean NOT NULL, active_version text
);
CREATE TABLE IF NOT EXISTS portfolio_rag.document_versions (
 doc_id text REFERENCES portfolio_rag.documents, version text, content_hash text NOT NULL,
 metadata jsonb NOT NULL, status text NOT NULL, created_at timestamptz DEFAULT now(),
 PRIMARY KEY(doc_id,version)
);
CREATE TABLE IF NOT EXISTS portfolio_rag.chunks (
 chunk_id text PRIMARY KEY, doc_id text, document_version text, title text NOT NULL,
 section text NOT NULL, category text NOT NULL, text text NOT NULL, source_url text,
 tags jsonb NOT NULL, content_hash text NOT NULL, token_count integer CHECK(token_count>0 AND token_count<=512),
 embedding vector(1024) NOT NULL, model_revision text NOT NULL,
 search_tsv tsvector GENERATED ALWAYS AS
 (to_tsvector('russian',coalesce(title,'')||' '||coalesce(section,'')||' '||text) ||
  to_tsvector('simple',coalesce(title,'')||' '||coalesce(section,'')||' '||text)) STORED,
 FOREIGN KEY(doc_id,document_version) REFERENCES portfolio_rag.document_versions
);
CREATE INDEX IF NOT EXISTS chunks_fts_idx ON portfolio_rag.chunks USING gin(search_tsv);
CREATE INDEX IF NOT EXISTS chunks_document_idx ON portfolio_rag.chunks(doc_id,document_version);
CREATE TABLE IF NOT EXISTS portfolio_rag.ingestion_runs (
 run_id text PRIMARY KEY, started_at timestamptz DEFAULT now(), status text NOT NULL,
 model_revision text NOT NULL, evidence jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS portfolio_rag.retrieval_events (
 id bigserial PRIMARY KEY, correlation_id text NOT NULL, event text NOT NULL,
 metadata jsonb NOT NULL, created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS portfolio_rag.rag_queries (
 correlation_id text PRIMARY KEY, session_hash text NOT NULL, mode text NOT NULL,
 fallback boolean NOT NULL, metrics jsonb NOT NULL, created_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS portfolio_rag.evaluation_runs (
 run_id text PRIMARY KEY, corpus_hash text NOT NULL, config jsonb NOT NULL,
 results jsonb NOT NULL, created_at timestamptz DEFAULT now()
);
CREATE OR REPLACE VIEW portfolio_rag.active_chunks AS
 SELECT c.*, d.case_id, c.title AS source_title, v.metadata->>'updated_at' AS updated_at FROM portfolio_rag.chunks c
 JOIN portfolio_rag.documents d ON d.doc_id=c.doc_id AND d.active_version=c.document_version
 JOIN portfolio_rag.document_versions v ON v.doc_id=c.doc_id AND v.version=c.document_version
 WHERE d.status='ACTIVE' AND d.public_safe=true AND v.status='ACTIVE'
 AND v.metadata->>'confidentiality'='public';

CREATE INDEX IF NOT EXISTS chunks_hnsw_idx ON portfolio_rag.chunks USING hnsw(embedding vector_cosine_ops) WITH(m=8,ef_construction=32);
