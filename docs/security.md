# Security boundaries

Приложение получает только возможность выполнить scoped CHAT_COMPLETION через compatible Broker. Raw API key, export, admin и arbitrary service access не требуются. Provider secret хранит и использует Broker, не приложение.

Public API проверяет Origin, body <=4096 bytes, message 2–1200 символов, session ID 12–96, mode и rate limits. Rate budget 20 запросов / 600 с на IP; one active worker. Host reverse proxy должен перезаписывать X-Real-IP и запрещать обход proxy: untrusted client header не является identity. Это prerequisite отдельно настраиваемого deployment, не автоматически обеспечиваемый standalone installer.

Memory ограничена TTL, capacity и длиной; reset или restart удаляет process-local контекст. Контакты и секретоподобный ввод отклоняются до генерации и memory. Диалог не становится trusted knowledge. Sources считаются untrusted; неподтверждённая, изменённая или опасная цитата отвергается сервером.

Reader DB role читает только active public-safe view. Telemetry role записывает обезличенные timings/counts/usage, без raw conversations. Admin credentials и публичный DB port приложению не нужны. Чат не выполняет произвольные действия, не отправляет leads и не обрабатывает платежи.

Injection probes, poisoned-context probe и public request guards прошли приёмку. Конечный набор тестов не гарантирует абсолютной защиты; новые модели, параметры и типы ввода требуют отдельного review и свежего unseen holdout.
