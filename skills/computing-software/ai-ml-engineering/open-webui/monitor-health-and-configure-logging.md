---
id: computing-software.ai-ml-engineering.open-webui.monitor-health-and-configure-logging
name: monitor-health-and-configure-logging
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [logging, monitoring, health-check, uptime-kuma, json-logs, log-level]
level: practitioner
status: docs-checked
description: "Set up three-level uptime monitoring for Open WebUI (/health, /api/models, real completion) and tune backend log level and JSON log format."
sources:
  - https://docs.openwebui.com/reference/monitoring
  - https://docs.openwebui.com/getting-started/advanced-topics/logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know when Open WebUI or its model providers break, and make logs usable.

## Monitoring levels
1. Liveness: `GET /health` is unauthenticated and returns 200 when the web server, app init and basic DB connectivity are fine. Uptime Kuma: HTTP(s) monitor, URL `http://your-open-webui-instance:8080/health`, interval 60 s, retries 3.
2. Model connectivity: `GET /api/models` needs `Authorization: Bearer YOUR_API_KEY`. Use a dedicated non-admin user (for example `monitoring-bot`) and its API key. Uptime Kuma: type "HTTP(s) - JSON Query", JSON query `$count(data[*])>0`, expected value `true`, interval 300 s. JSONata examples: `$count(data[owned_by='ollama'])>0`, `$exists(data[id='<model-id>'])`, `$count(data[id in ['a','b']]) = 2`.
3. Deep check: POST `/api/chat/completions` with a JSON body such as `{"messages":[{"role":"user","content":"Respond with the word HEALTHY"}],"model":"<model-id>","temperature":0}` and the same bearer header; validate that the reply contains HEALTHY. This catches model load failures and provider problems that levels 1 and 2 miss.

## Logging
Frontend: browser DevTools console (F12 or Cmd+Option+I). Backend: Python `logging` to stdout at INFO by default (visible via `docker logs`).

- `GLOBAL_LOG_LEVEL`: one of `CRITICAL` (50), `ERROR` (40), `WARNING` (30), `INFO` (20, default), `DEBUG` (10). It reconfigures the root Python logger with `logging.basicConfig(force=True)`, so it affects third-party libraries too. Docker: `--env GLOBAL_LOG_LEVEL="DEBUG"`; Compose: `- GLOBAL_LOG_LEVEL=DEBUG`.
- Cost: filtered-out messages are never built, so higher levels save work. `WARNING` also drops the retrieval results logged on every chat that uses a knowledge base. `DEBUG` is the most expensive and logs whole chat request payloads; set it back after troubleshooting.
- `LOG_FORMAT=json` switches all stdout to single-line JSON for Loki, Datadog, CloudWatch. Fields: `ts` (ISO 8601), `level` (`debug`, `info`, `warn`, `error`, `fatal`), `msg`, `caller` (`module:function:line`), `extra`, `error`, `stacktrace`. The ASCII banner is suppressed so the stream stays parseable; covers early startup (stdlib logging) and runtime (Loguru). Without `LOG_FORMAT`, output is plain text.

## Gotcha
Open WebUI can be healthy while the model provider is down, so level 1 alone is not enough.

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages reference/monitoring and getting-started/advanced-topics/logging (both read in full): the three monitoring levels with /health unauthenticated, /api/models bearer auth, the Uptime Kuma settings, JSONata examples, the deep check body and what it catches, frontend console and backend stdout at INFO, the five log levels and values, GLOBAL_LOG_LEVEL via basicConfig(force=True) with the Docker and Compose forms, the log-level cost note, and LOG_FORMAT=json fields, banner suppression and early-plus-runtime coverage. Nothing removed.
Method: documentation only; no commands were run.
