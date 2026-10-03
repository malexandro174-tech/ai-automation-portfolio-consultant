---
doc_id: tech-rag
title: 'RAG: подход и подтверждённый опыт'
category: technology
source_type: sanitized_public_summary
source_url: https://ai.mag-astro.ru/knowledge/tech-rag
updated_at: '2026-10-03'
version: 1.0.2
confidentiality: public
public_safe: true
tags:
- RAG
- Qdrant
- BGE-M3
- technology
case_type: capability_summary
technologies:
- RAG
- Qdrant
- BGE-M3
case_id: null
---
# RAG: подход и подтверждённый опыт

## Что делает RAG
RAG соединяет поиск по базе знаний и генерацию ответа по найденному контексту. Векторный поиск использует embeddings, а источники позволяют проверить фактические утверждения.
## Подтверждённый кейс
Writer OS RAG имеет контракты индексации и запросов, использует Qdrant и локальную модель BGE-M3. Его корпус относится к отдельной предметной области и не смешивается с публичным коммерческим портфолио.
## Public FAQ
Предыдущая версия публичного FAQ v1 использовала совпадение токенов в структурированных FAQ и текстовых записях. Она извлекала готовый ответ и не являлась полноценным vector RAG. Этот раздел фиксирует исторический подход; текущий публичный RAG v2 и результаты его приёмки описаны в README репозитория.
