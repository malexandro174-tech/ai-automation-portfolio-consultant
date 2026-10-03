---
doc_id: case-data-analyst
title: AI Data Analyst Workspace
category: portfolio
source_type: public_readme_summary
source_url: https://ai.mag-astro.ru/knowledge/case-data-analyst
updated_at: '2026-10-02'
version: 1.0.1
confidentiality: public
public_safe: true
tags:
- Python
- FastAPI
- DeepSeek
- Docker
- portfolio
case_type: implemented
technologies:
- Python
- FastAPI
- DeepSeek
- Docker
case_id: case-data-analyst
---
# AI Data Analyst Workspace

## Проблема
Табличные данные требуют просмотра структуры, расчёта метрик, построения графиков и подготовки отчёта. Разрозненные инструменты усложняют этот процесс.
## Реализованное решение
AI Data Analyst Workspace объединяет загрузку CSV, XLSX, XLS и JSON, проверяемый анализ данных, графики и отчёты. Поддерживаются PNG, JPEG и WEBP для visual analysis.
## Возможности
Локальные инструменты вычисляют структуру, пропуски, уникальные значения и числовые метрики. Есть line, bar, histogram, scatter и pie charts. DOCX-отчёт и Markdown summary регистрируются как скачиваемые артефакты.
## Безопасность и ограничения
LLM получает ограниченный data context и формирует валидированный план. Pandas, matplotlib и python-docx выполняют расчёты; произвольный код модели не исполняется. Файлы изолированы по сессии, полный набор данных не передаётся LLM.
