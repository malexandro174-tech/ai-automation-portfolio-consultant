---
doc_id: case-public-consultant
title: Public FAQ / AI Consultant
category: portfolio
source_type: sanitized_public_summary
source_url: https://ai.mag-astro.ru/knowledge/case-public-consultant
updated_at: '2026-10-03'
version: 1.0.2
confidentiality: public
public_safe: true
tags:
- FastAPI
- Docker
- Nginx
- portfolio
case_type: implemented
technologies:
- FastAPI
- Docker
- Nginx
case_id: case-public-consultant
---
# Public FAQ / AI Consultant

## Проблема
Посетителю портфолио нужен первый ответ о компетенциях, реализованных кейсах и процессе без выдуманных цен, сроков и гарантий.
## Реализованное решение v1
Историческая версия Public FAQ / AI Consultant работала на ai.mag-astro.ru через FastAPI и web-виджет. Она использовала структурированные FAQ и текстовые записи, поиск по совпадению токенов и извлечение готового ответа.
## Память и передача интереса
Есть ограниченная анонимная process-local память, fallback и защита от некоторых prompt injection запросов. Коммерческий интерес показывает кнопку существующей формы; заявка отправляется только пользователем.
## Ограничения
Историческая версия FAQ v1 не использовала embeddings, векторную базу или LLM-generation. Её API возвращал ссылки на исходные материалы, а виджет не показывал полноценный список citations. Этот раздел описывает предшественник продукта; текущий публичный RAG v2 описан в README репозитория.
