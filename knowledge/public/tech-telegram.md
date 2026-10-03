---
doc_id: tech-telegram
title: Telegram-боты
category: technology
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/tech-telegram
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Telegram
- Broker
- technology
case_type: capability_summary
technologies:
- Telegram
- Broker
case_id: null
---
# Telegram-боты

## Диалоговые сценарии
AI Lead Intake & Qualification Assistant ведёт Telegram-диалог, собирает обязательные данные, валидирует заявку, рассчитывает fit score и передаёт структурированный лид оператору. Состояние сохраняется в SQLite.
## Обучение сотрудников
AI Employee Training & Certification Assistant использует Telegram для учебных блоков, вопросов, тестирования и обратной связи. Активная сессия и результаты сохраняются в PostgreSQL.
## Доступ
В описанных ассистентах внешние вызовы Telegram и AI выполняются через Credential / Access Broker. Приложения не получают произвольные цели доставки и raw provider credentials. Наличие TEST-delivery не доказывает массовую production-рассылку.
