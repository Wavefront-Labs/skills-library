---
id: computing-software.ai-ml-engineering.open-webui.export-opentelemetry-traces-and-metrics
name: export-opentelemetry-traces-and-metrics
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [opentelemetry, otel, grafana, tracing, metrics, observability]
level: practitioner
status: docs-checked
description: "Send Open WebUI traces, metrics and logs to an OTLP collector or the Grafana LGTM stack with the ENABLE_OTEL family of variables."
sources:
  - https://docs.openwebui.com/reference/monitoring/otel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: export traces, HTTP metrics and logs over OTLP.

## Fast path
```bash
curl -fsSLO https://docs.openwebui.com/docker-compose.otel.yaml
docker compose -f docker-compose.otel.yaml up -d
```
Starts `lgtm` (Grafana LGTM: UI on 3000, OTLP gRPC 4317, HTTP 4318) and `open-webui` (host 8088 to container 8080). Open WebUI at http://localhost:8088, Grafana at http://localhost:3000 (`admin` / `admin`). From inside the Compose network Open WebUI sends to `http://lgtm:4317`.

## Variables
- `ENABLE_OTEL` (master switch), `ENABLE_OTEL_TRACES`, `ENABLE_OTEL_METRICS`, `ENABLE_OTEL_LOGS`: all set true in the Compose file.
- `OTEL_EXPORTER_OTLP_ENDPOINT` (traces), `OTEL_METRICS_EXPORTER_OTLP_ENDPOINT`, `OTEL_LOGS_EXPORTER_OTLP_ENDPOINT`.
- `OTEL_EXPORTER_OTLP_INSECURE=true` for no TLS (consider removing in production).
- `OTEL_SERVICE_NAME` default `open-webui`.
- `OTEL_METRICS_EXPORT_INTERVAL_MILLIS` default `10000` (about 6 data points/min; `60000` for about 1).
- `OTEL_BASIC_AUTH_USERNAME` / `OTEL_BASIC_AUTH_PASSWORD` when the collector needs Basic Auth.
- `OTEL_PYTHON_FASTAPI_EXCLUDED_URLS` or `OTEL_PYTHON_EXCLUDED_URLS`: comma-separated regexes matched anywhere in the URL, excluding routes from traces and HTTP metrics, e.g. `/health,/_app/immutable/.*` (also covers `/health/db`).

## External collector
```bash
docker run -d --name open-webui -p 8088:8080 \
  -e ENABLE_OTEL=true -e ENABLE_OTEL_TRACES=true -e ENABLE_OTEL_METRICS=true \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317 -e OTEL_EXPORTER_OTLP_INSECURE=true \
  -e OTEL_METRICS_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317 \
  -e OTEL_LOGS_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317 \
  -e OTEL_SERVICE_NAME=open-webui -v open-webui:/app/backend/data ghcr.io/open-webui/open-webui:main
```

## What you get
Automatic instrumentation of FastAPI routes, SQLAlchemy queries, Redis, and `requests`/`httpx`/`aiohttp` calls. Spans carry `db.instance`, `db.statement`, `redis.args`, `http.url`, `http.method`, `http.status_code` and error details. Metrics: `http.server.requests` (counter) and `http.server.duration` (histogram, ms), labelled `http.method`, `http.route`, `http.status_code`.

## Gotchas and troubleshooting
- For pip or source installs the OTel packages may be missing: `pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp`.
- Nothing in Grafana: check all three ENABLE_ flags, that the endpoint resolves from inside the Open WebUI container, container logs for OTLP errors, and that port 4317 is reachable (`curl http://localhost:4317`).
- With TLS to the collector, adjust or remove `OTEL_EXPORTER_OTLP_INSECURE`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/monitoring/otel (read in full): the Compose quick start and its curl and up commands, lgtm and open-webui ports, the Grafana admin login and lgtm:4317 endpoint, every listed variable and default, the exclusion variables and regex matching, the external collector docker run, the pip dependency warning, the automatic instrumentation and span attributes, the two metrics and their labels, and the troubleshooting list. Nothing removed.
Method: documentation only; no commands were run.
