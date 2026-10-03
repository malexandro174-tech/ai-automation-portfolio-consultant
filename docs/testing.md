# Tests and evidence

## Fresh local regression — 3 октября 2026

`python -m pytest -q`: **69 passed**. Проверены memory TTL/capacity, follow-up normalization, unsupported/forged sources, matcher validation, policy/PII fallback before provider, provider failures, output boundaries, public request guards, reset и rate limits. Test doubles не обращаются к production DB, BGE, Broker или DeepSeek. Свежий результат записан в [local-regression.json](evidence/local-regression.json).

## Production acceptance — 2 октября 2026

[Public-safe results](evidence/production-acceptance.json): новый synthetic holdout создан после freeze retrieval/prompt parameters; 20 interactions, 19 correct, factual 10/10, source support 20/20, critical 0, injection 2/2. Cases не содержат настоящих посетителей, session IDs, private correlation IDs или secrets. Public HTTP latency: 20 uncached WAN queries, P95 5.50 с, max 6.12 с.

App rollback к FAQ v1 — 3.83 с; отдельно full app/proxy/symlink rollback — 3.77 с. Resource admission PASS для concurrency 1. Эти historical measurements не запускались повторно при GitHub publication.

Один ambiguous question не запросил уточнение; case не зачтён и не скрыт. Parameters не ретюнились по набору. Exact-quote support и synthetic accuracy не доказывают пользу всей аудитории. Два editorial KB changes public copy не выдаются за новую production evaluation.

## Publication checks

Перед push: allowlisted source selection, secret/PII/private-path/infra scan, link checks, UTF-8, syntax, knowledge hashes и screenshot review. После push: публичный README, badges, Mermaid, screenshots, About/topics, visibility и release проверяются через GitHub API и browser. Full internal operational reports не публикуются.
