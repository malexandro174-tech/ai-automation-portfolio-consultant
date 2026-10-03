# Local development and integration

Offline tests запускаются после `python -m pip install -e ".[test]"`; production systems, provider keys, real leads и SQL mutations им не нужны.

Для отдельной интеграции нужны: pinned BGE-M3/TEI со 1024 dimensions и лимитом 512 tokens, populated PostgreSQL 17 + pgvector schema, отдельные reader/telemetry роли, compatible Access & Integration Broker и host FastAPI/proxy/widget integration. Private Broker, secret storage, corpus ingestion и production Compose не распространяются.

Settings публичных adapters: RAG_TEI_URL, RAG_BROKER_URL, RAG_BROKER_REQUESTER, RAG_DB_HOST, RAG_DB_PORT, RAG_DB_NAME, RAG_READER_USER, RAG_TELEMETRY_USER, RAG_READER_PASSWORD_FILE, RAG_TELEMETRY_PASSWORD_FILE, RAG_PUBLIC_ORIGIN. Значения задаёт отдельный владелец deployment; их нельзя коммитить. App не получает DeepSeek key. За provisioning, роли, сети, proxy и повторную resource/quality admission отвечает deployment owner.

API factory принимает уже сконфигурированный service. Она не подключается автоматически к чужой инфраструктуре. Widget fragment использует host-page design tokens и #contact. Source links и knowledge pages относятся к публичному домену MAG; адаптация для другого портфолио требует новых документов, model fingerprint и приёмки.

Это source/integration distribution; clone → live standalone run не заявляется. Публикация не изменяет текущий public runtime.
