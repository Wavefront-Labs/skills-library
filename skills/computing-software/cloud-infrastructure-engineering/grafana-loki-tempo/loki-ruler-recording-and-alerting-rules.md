---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-ruler-recording-and-alerting-rules
name: loki-ruler-recording-and-alerting-rules
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-ruler-rules, loki, ruler, recording-rules, alerting-rules, remote-write, alertmanager]
level: practitioner
status: docs-checked
description: "Define LogQL alerting and recording rules in the Loki ruler, send alerts to Alertmanager and recorded series to remote write."
sources: ["https://grafana.com/docs/loki/latest/alert/", "https://grafana.com/docs/loki/latest/reference/loki-http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: alerts from logs and derived metrics stored in Prometheus or Mimir.

Rule files use the Prometheus rule format with LogQL expressions:
```yaml
groups:
  - name: api-errors
    rules:
      - alert: HighPercentageError
        expr: sum(rate({app="api"} |= "error" [5m])) by (job) / sum(rate({app="api"}[5m])) by (job) > 0.05
        for: 10m
        labels:
          severity: page
        annotations:
          summary: "High error ratio"
      - record: nginx:requests:rate1m
        expr: sum(rate({container="nginx"}[1m]))
```
Ruler configuration from the docs (local rule storage):
```yaml
ruler:
  storage:
    type: local
    local:
      directory: /tmp/rules
  rule_path: /tmp/scratch
  alertmanager_url: http://localhost
  ring:
    kvstore:
      store: inmemory
  enable_api: true
```
Recording rules write to a Prometheus-compatible remote-write endpoint (Prometheus 2.25 or later, Mimir, Thanos Receiver):
```yaml
ruler:
  remote_write:
    enabled: true
    clients:
      mimir:
        url: http://mimir:9009/api/v1/push
```
Loki adds `X-Scope-OrgID` with the tenant ID automatically; do not set it under `headers`.

Manage rules via the API (`enable_api: true`): `POST /loki/api/v1/rules/{namespace}` (body `Content-Type: application/yaml`, returns 202), `GET /loki/api/v1/rules`, `DELETE /loki/api/v1/rules/{namespace}/{groupName}`. Or use `lokitool rules diff|sync|print|format` (needs `--id=` tenant ID or `LOKI_TENANT_ID`; `fake` in single-tenant mode); Loki before 3.1 used `cortextool`.

## Verify
```
curl http://loki:3100/loki/api/v1/rules
curl http://loki:3100/prometheus/api/v1/alerts
```
Rules and active alerts are listed.

## Checked
2026-11-03. Confirmed against the Loki "Alerting and recording rules" page and the HTTP API reference (rules and alerts endpoints, 202, YAML content type). Corrected: `remote_write` takes a `clients:` map, not `client:`; `mimirtool` replaced by `lokitool`. Removed: the `<rules_dir>/<tenant>/rules.yaml` path claim, the `interval` key, and the "same limits as normal queries" and per-tenant evaluation gotchas (not on the pages read).
Method: documentation only; no commands were run.
