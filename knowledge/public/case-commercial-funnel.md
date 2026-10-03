---
doc_id: case-commercial-funnel
title: Commercial Funnel Observability
category: portfolio
source_type: sanitized_public_summary
source_url: https://ai.mag-astro.ru/knowledge/case-commercial-funnel
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Python
- PostgreSQL
- observability
- portfolio
case_type: implemented
technologies:
- Python
- PostgreSQL
- observability
case_id: case-commercial-funnel
---
# Commercial Funnel Observability

## Проблема
Несколько источников заказов требуют понятного пути от поиска и оценки до shortlist, а также контроля состояния источников и обработки.
## Реализованное решение
Commercial Funnel Observability использует read-only discovery, Fit/Risk-пайплайн и shortlist. Добавлены correlation ID, структурированные redacted events, PostgreSQL-метрики и source health.
## Границы
Отклики не отправляются автоматически. Система не является автономным sales closer и не гарантирует заключение сделок. Клиентские данные и приватные коммерческие сообщения не включаются в публичный кейс.
