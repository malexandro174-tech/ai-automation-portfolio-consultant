---
doc_id: case-lead-intake
title: AI Lead Intake & Qualification Assistant
category: portfolio
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/case-lead-intake
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Telegram
- SQLite
- Broker
- DeepSeek
- portfolio
case_type: implemented
technologies:
- Telegram
- SQLite
- Broker
- DeepSeek
case_id: case-lead-intake
---
# AI Lead Intake & Qualification Assistant

## Проблема
Первичный сбор обращений требует уточнить задачу, контакты и желаемый результат, проверить полноту и передать структурированный лид оператору.
## Реализованное решение
AI Lead Intake & Qualification Assistant ведёт Telegram-диалог, валидирует данные, рассчитывает fit score и сохраняет заявки и сессии в SQLite. Доступны команды /start, /reset и /help.
## Данные и передача
Обязательные поля — имя, контакт, задача и желаемый результат. Необязательные ответы можно пропустить или отметить как неизвестные. Карточка лида передаётся через ограниченный Credential / Access Broker.
## Ограничения
README описывает TEST-delivery в зарегистрированную цель. Это не подтверждение массовой production-рассылки, текущего клиента или внедрения в конкретную CRM. При недоступном Broker запрос безопасно завершается ошибкой.
