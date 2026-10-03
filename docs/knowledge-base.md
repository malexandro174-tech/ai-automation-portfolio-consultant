# Knowledge base

25 документов, one topic per document: faq, portfolio, process, profile, security, services, technology. Metadata и manifest обеспечивают происхождение, public-safe статус, версии и content hashes. Case IDs относятся к публичным portfolio описаниям; это не клиентские IDs.

При production acceptance каждый документ дал один active chunk; точный 512-token embedding limit обеспечивает TEI, silent truncation запрещена. Context использует сохранённые token_count. Source pages открывают конкретный документ.

Public corpus 1.0.2 повторяет подтверждённые материалы и уточняет исторический контекст двух документов о FAQ v1. Accepted production corpus 1.0.1 этой publication wave не изменялся. Не следует повторно выдавать результаты старого holdout как оценку редакционно изменённого нового корпуса.

Перед update: проверка секретов, PII и приватных данных, review фактов, version bump и hash update. Deployment обновлённой KB — отдельная работа с новой приёмкой. Ни private planning, ни реальные leads, ни raw conversations в репозитории не хранятся.
