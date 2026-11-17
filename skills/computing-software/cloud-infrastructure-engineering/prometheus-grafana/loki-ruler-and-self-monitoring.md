---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-ruler-and-self-monitoring
name: loki-ruler-and-self-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki, loki-ruler, loki-alert-rules, loki-recording-rules, ruler-remote-write, loki-metrics, loki-dashboards, loki-mixin, logql-alert-queries, loki-alerting-queries]
level: advanced
status: verified
description: "Alert and record from logs with the Loki ruler (rule files, remote write of recording rules, Alertmanager), write alert-grade LogQL, and monitor Loki with its mixin."
sources: ["https://grafana.com/docs/loki/latest/alert/", "https://grafana.com/docs/loki/latest/operations/meta-monitoring/", "https://github.com/grafana/loki/tree/main/production/loki-mixin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki ruler and self-monitoring

## Ruler config
```yaml
ruler:
  storage: {type: s3, s3: {bucketnames: loki-ruler}}     # or local: {directory: /etc/loki/rules}
  rule_path: /tmp/loki-rules-scratch
  alertmanager_url: http://alertmanager.monitoring:9093
  enable_api: true
  enable_alertmanager_v2: true
  remote_write:
    enabled: true
    client: {url: http://mimir-nginx/api/v1/push, headers: {X-Scope-OrgID: logs-derived}}
  wal: {dir: /loki/ruler-wal}
```
Rules are Prometheus-format files per tenant (`/rules/<tenant>/*.yaml` locally; with `auth_enabled: false` the tenant is `fake`) or loaded with
`lokitool rules sync --address=... --id=<tenant>` (`lokitool rules diff|load|sync|lint`). `mimirtool rules ... --backend=loki` no longer works: mimirtool 3.2.2 accepts only `--backend=mimir`.

## Rules
```yaml
groups:
  - name: checkout-logs
    interval: 1m
    rules:
      - record: namespace:loki_error_lines:rate1m
        expr: sum by (namespace) (rate({cluster="prod"} |= "level=error" [1m]))
      - alert: PaymentGatewayTimeouts
        expr: |
          sum by (namespace) (count_over_time({app="checkout"} |= "gateway timeout" [5m])) > 20
        for: 5m
        labels: {severity: page, team: payments}
        annotations: {summary: "{{ $labels.namespace }}: {{ $value }} gateway timeouts in 5m"}
```
## Alert-grade LogQL
- Use metric queries (`count_over_time`, `rate`, `sum by`) with a **tight stream selector** (labels, not just
  line filters) and short ranges; rules run every interval for the life of the alert.
- Prefer line filters (`|=`) before parsers; parse only when you need a label for `by` or an unwrap.
- Ratios: `sum(rate({app="x"} |= "error"[5m])) / sum(rate({app="x"}[5m]))`.
- Recording rules + remote write turn expensive log metrics into cheap Prometheus series for dashboards.

## Monitoring Loki
Install the loki-mixin dashboards (the compiled mixin has Operational, Writes, Reads, Chunks, Retention, Deletion and more) and alerts
(`LokiRequestErrors`, `LokiRequestLatency`, `LokiRequestPanics`, `LokiTooManyCompactorsRunning`, `LokiCompactorHasNotSuccessfullyRunCompaction`). Key metrics:
`loki_request_duration_seconds` by route, `loki_ingester_memory_streams`, `loki_distributor_bytes_received_total`,
`loki_discarded_samples_total`, `loki_ruler_wal_*`, `loki_compactor_*`. Meta-monitoring: ship Loki's own logs and
metrics to a separate stack, so an outage is still visible.

## Verify
- [ ] `GET /loki/api/v1/rules` lists the groups; firing alerts appear in Alertmanager.
- [ ] Recording rule series queryable in Mimir/Prometheus.

## Checked
Ran Loki 3.7.9 with the page's ruler config (local storage, `alertmanager_url`, `enable_alertmanager_v2`, `remote_write` client with an `X-Scope-OrgID` header, `wal.dir`) against Alertmanager 0.34.1 and Prometheus 3.15.1 (remote-write receiver) on localhost, and the page's rule file under `rules/fake/`: `GET /loki/api/v1/rules` listed the group, the alert fired into Alertmanager's `/api/v2/alerts` with the templated summary (`prod: 19 gateway timeouts in 5m`), and the recording rule `namespace:loki_error_lines:rate1m` was queryable in Prometheus. The S3 ruler-storage form loaded with `-verify-config`. `lokitool` 3.7.9 `rules diff|sync|load|lint` exist and `diff` reached the ruler API; `mimirtool rules list --backend=loki` failed with `enum value must be one of mimir`. `loki_request_duration_seconds`, `loki_ruler_wal_*`, `loki_ingester_memory_streams`, `loki_distributor_bytes_received_total`, `loki_discarded_samples_total`, `loki_compactor_*` exist on `/metrics`; mixin alert and dashboard names were read from `production/loki-mixin-compiled` at tag v3.7.9.
