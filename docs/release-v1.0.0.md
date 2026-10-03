# v1.0.0 — Production RAG Portfolio Consultant

## Что это

Публичный RAG-консультант по AI-автоматизации и подтверждённым кейсам MAG: ответы с источниками и подбор похожих решений.

## Что умеет

Grounded ответы, source pages, до трёх Solution Matcher карточек, технологии, объяснение релевантности, уточнения, bounded follow-up/reset и optional CTA к существующей форме без automatic send.

## Архитектура

FastAPI → BGE-M3 → PostgreSQL/pgvector + FTS → RRF → context → compatible Broker → DeepSeek → exact answer validator. Production переиспользует existing app и BGE; DB dedicated. Public source package содержит конфигурируемые adapters, а не private infrastructure.

## Knowledge Base

25 public-safe Markdown docs. Production acceptance corpus 1.0.1; repository public copy 1.0.2 уточняет историческое описание FAQ v1 без production ingestion.

## Acceptance

Измерения 2026-10-02: frozen holdout 19/20, factual 10/10, source support 20/20, critical hallucinations 0; P95 5.50 с и max 6.12 с на 20 uncached public запросах; app rollback 3.83 с. Injection и resource gate PASS. Fresh offline regression 2026-10-03: 69 passed.

## Security

Broker-only scoped CHAT_COMPLETION; app без raw credentials, request/rate/session bounds, exact source validation, anonymous telemetry, no automatic lead submission. Private configs, dumps, client data и operational recovery не опубликованы.

## Demo

https://ai.mag-astro.ru/ — production public RAG v2. README содержит реальные screenshots и примеры вопросов.

## Limitations

Small synthetic sample не доказывает будущую audience accuracy; один ambiguous UX gap; business usefulness не измерена; concurrency 1; внешняя model availability и KB review. Standalone deployment без configured Broker/TEI/DB пока не предоставляется. Publication не изменяет production.
