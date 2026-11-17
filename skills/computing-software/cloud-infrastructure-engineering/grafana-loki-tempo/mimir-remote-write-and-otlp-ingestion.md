---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-remote-write-and-otlp-ingestion
name: mimir-remote-write-and-otlp-ingestion
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [mimir-remote-write, mimir, prometheus-remote-write, otlp-metrics, distributor, push-endpoint, otel-collector]
level: practitioner
status: docs-checked
description: "Send Prometheus remote write or OTLP metrics to Mimir through an OpenTelemetry Collector or directly, with tenant header, basic auth and label conversion rules."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-otel-collector/", "https://grafana.com/docs/mimir/latest/references/http-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reliable metric ingestion with correct tenancy.

Endpoints on the distributor (both need authentication, meaning the `X-Scope-OrgID` header carrying the tenant ID unless multi-tenancy is disabled):
- `POST /api/v1/push`: Prometheus remote write, protobuf with Snappy, header `X-Prometheus-Remote-Write-Version: 0.1.0`.
- `POST /otlp/v1/metrics`: OTLP over HTTP, protobuf optionally GZIP-compressed.

The docs recommend OTLP when you use the OpenTelemetry Collector. Collector config, OTLP:
```yaml
extensions:
  basicauth/otlp:
    client_auth:
      username: username
      password: password
exporters:
  otlphttp:
    auth:
      authenticator: basicauth/otlp
    endpoint: http://<mimir-endpoint>/otlp
service:
  extensions: [basicauth/otlp]
  pipelines:
    metrics:
      receivers: [...]
      processors: [...]
      exporters: [otlphttp]
```
Remote write instead: the `prometheusremotewrite` exporter with `endpoint: http://<mimir-endpoint>/api/v1/push` (same `basicauth` extension pattern).

Labels and formats
- Dots and dashes in metric and label names become `_` (`http.status_code` becomes `http_status_code`).
- Resource attributes go to a `target_info` series (query with a join or the Prometheus `info()` function); `service.namespace/service.name` (or `service.name`) becomes `job` and `service.instance.id` becomes `instance`.
- `-distributor.otel-promote-resource-attributes` (experimental) promotes chosen resource attributes to labels at ingestion.
- OpenTelemetry Exponential Histograms are rejected unless native histogram ingestion is enabled first (see Mimir's native histogram page); then they convert to native histograms.
- `-api.skip-label-name-validation-header-enabled=true` plus header `X-Mimir-SkipLabelNameValidation: true` skips label name validation for non-compliant clients.

## Verify
Query the tenant with the same `X-Scope-OrgID` header and confirm the series arrive.

## Checked
2026-11-03. Confirmed against the Mimir OpenTelemetry Collector page and HTTP API reference (push and OTLP endpoints, authentication header). Removed: Prometheus `remote_write` YAML (queue tuning, `send_exemplars`), the Alloy snippet, the `/otlp` endpoint wording for generic collectors, the 429 and 400 gotchas, the cumulative temporality claim, and the `prometheus_remote_storage_samples_failed_total` check, none of which are on the Mimir pages read.
Method: documentation only; no commands were run.
