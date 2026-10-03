---
doc_id: case-intake-classifier
title: AI Intake Classifier
category: portfolio
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/case-intake-classifier
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- n8n
- NocoDB
- Telegram
- JSON
- portfolio
case_type: implemented
technologies:
- n8n
- NocoDB
- Telegram
- JSON
case_id: case-intake-classifier
---
# AI Intake Classifier

## Проблема
Ручная классификация обращений замедляет triage и может пропустить срочные жалобы. Нужны понятная категория, приоритет и маршрут обработки.
## Реализованное решение
AI Intake Classifier — workflow n8n: webhook, AI-классификация, JSON validation, приоритет, routing, NocoDB и Telegram alert. Категории включают Lead, Support, Complaint и Product Question.
## Результат
Workflow выдаёт структурированную запись с приоритетом low, normal, high или critical. Жалобы и критические случаи могут эскалироваться в Telegram. Экспорт workflow предназначен для повторного использования без встроенных секретов.
## Ограничения
CRM adapters, SLA routing и analytics dashboard перечислены в roadmap. Эти функции не следует объявлять уже реализованными. Не заявляется измеренный рост продаж или точность классификации без отдельного результата тестов.
