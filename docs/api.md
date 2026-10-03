# Public API contracts

POST `/api/v2/portfolio-consultant/chat`: session_id, message и mode (`auto`, `qa`, `solution_matcher`). Response: answer, sources, matched_cases, fallback/reason, timings, usage, lead_handoff и auto_send=false. Factual sources включают document title, public URL и version. Ошибки input/Origin/rate/busy обрабатываются до pipeline.

POST `/api/v2/portfolio-consultant/session/clear`: session_id, process-local reset. GET `/knowledge/{slug}`: фиксированная public source page. Endpoints operator admission и secrets не входят в public package.

Visitor вводит контакты только в существующей форме host site. Чат не создаёт второй lead store и не отправляет форму от его имени. Monetary cost поля могут быть null: actual token usage измеряется отдельно, USD forecasts считаются offline.
