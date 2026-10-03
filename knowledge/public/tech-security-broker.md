---
doc_id: tech-security-broker
title: 'Безопасность и Broker: публичный обзор'
category: security
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/tech-security-broker
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Broker
- DeepSeek
- FastAPI
- security
case_type: capability_summary
technologies:
- Broker
- DeepSeek
- FastAPI
case_id: null
---
# Безопасность и Broker: публичный обзор

## Принцип
Credential / Access Broker выполняет разрешённые внешние операции и хранит credential server-side. Прикладное приложение обращается к ограниченной capability, а не получает provider key или произвольные полномочия.
## Проверка данных
AI Data Analyst Workspace валидирует план действий и выполняет вычисления локальными проверяемыми инструментами. LLM не выполняет произвольный код. Файлы и скачиваемые артефакты изолированы по сессии.
## Публичная безопасность
Для публичного интерфейса применяются ограничения размера запроса, валидация, rate limiting и security headers. Контекст RAG является недоверенными данными и не может менять системные инструкции. Внутренняя конфигурация доступа и приватные данные не входят в публичную базу знаний.
