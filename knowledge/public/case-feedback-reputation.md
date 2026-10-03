---
doc_id: case-feedback-reputation
title: AI Customer Feedback & Reputation Agent
category: portfolio
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/case-feedback-reputation
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- DeepSeek
- PostgreSQL
- Docker
- Broker
- portfolio
case_type: implemented
technologies:
- DeepSeek
- PostgreSQL
- Docker
- Broker
case_id: case-feedback-reputation
---
# AI Customer Feedback & Reputation Agent

## Проблема
Клиентские отзывы нужно классифицировать по тональности и риску, подготовить ответ и передать сложные или опасные случаи оператору.
## Реализованное решение
AI Customer Feedback & Reputation Agent принимает отзывы через SandboxReviewSource. Rule-prefilter и DeepSeek классифицируют тональность и риск. PostgreSQL хранит очередь, попытки и состояния обработки.
## Контроль ответа
Политики ответа — AUTO_SAFE, APPROVAL_REQUIRED и BLOCKED. Рискованные обращения требуют контроля; уведомления ограничены зарегистрированным TEST-target через Broker. Операторская сводка показывает операционное состояние.
## Ограничения
Первый источник является sandbox. Кейс не подтверждает готовое подключение к произвольному marketplace и не доказывает автоматическую публикацию ответов реальным клиентам. Для новой интеграции нужно уточнить источник отзывов и правила согласования.
