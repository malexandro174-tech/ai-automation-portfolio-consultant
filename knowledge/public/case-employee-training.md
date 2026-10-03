---
doc_id: case-employee-training
title: AI Employee Training & Certification Assistant
category: portfolio
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/case-employee-training
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Telegram
- PostgreSQL
- DeepSeek
- Python
- portfolio
case_type: implemented
technologies:
- Telegram
- PostgreSQL
- DeepSeek
- Python
case_id: case-employee-training
---
# AI Employee Training & Certification Assistant

## Проблема
Внутренние правила могут оставаться в документах без измеримой проверки того, что сотрудник их понял.
## Реализованное решение
AI Employee Training & Certification Assistant ведёт сотрудника по коротким learning-блокам, отвечает по материалу, проводит тестирование и даёт обратную связь. Интерфейс работает в Telegram.
## Результаты
Система использует пять настраиваемых вопросов, explainable score и статусы CERTIFIED, RETRAINING_RECOMMENDED и NOT_READY. PostgreSQL сохраняет сессии и результаты, поддерживая восстановление активного диалога.
## Ограничения
Telegram и LLM доступны через Credential / Access Broker. Ответы ограничены переданным материалом. Публичное описание не подтверждает текущего заказчика, массовое production-внедрение или юридическую силу сертификата.
