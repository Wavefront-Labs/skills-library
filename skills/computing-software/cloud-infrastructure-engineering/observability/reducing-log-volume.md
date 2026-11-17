---
id: computing-software.cloud-infrastructure-engineering.observability.reducing-log-volume
name: reducing-log-volume
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-volume-reduction, adaptive-logs, observability-cost, log-sampling, structured-logging]
level: practitioner
status: draft
description: "Cut log ingest cost: measure volume by source, drop and sample at the agent, demote noisy levels, shorten verbose lines, and use Grafana Adaptive Logs pattern drops."
sources: ["https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/logs-costs/", "https://grafana.com/docs/grafana-cloud/cost-management-and-billing/reduce-costs/logs-costs/adaptive-logs/", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing log volume

## 1. Measure first
- Loki: `sum by (service_name) (bytes_over_time({service_name=~".+"}[1h]))` or the volume API / Logs Drilldown.
- Grafana Cloud: Usage insights / billing dashboards show GB per stream selector.
- Patterns: Loki `pattern` detection (`/loki/api/v1/patterns`) shows which message templates dominate. Typically
  5-10 patterns are 50-80% of volume (health checks, access logs, debug loops).

## 2. Drop at the agent (cheapest place)
Alloy:
```alloy
loki.process "drop_noise" {
  forward_to = [loki.write.default.receiver]
  stage.drop { expression = ".*GET /healthz.*" }
  stage.drop { source = "level" value = "debug" }
  stage.drop { older_than = "24h" drop_counter_reason = "too_old" }
  stage.sampling { rate = 0.1 }               // keep 10%; put inside stage.match for one stream
}
```
OTel Collector: `filter` processor with `log_conditions: ['severity_number < SEVERITY_NUMBER_INFO']`, or
`probabilistic_sampler` on logs (`sampling_percentage: 10`, `attribute_source: record` to keep all lines of a trace).

## 3. Fix at source
- Default production level INFO; demote per-request success logs to DEBUG.
- Remove multi-KB payload dumps; log IDs not bodies.
- Rate-limit repetitive errors (log once per N seconds with a count).
- Access logs: sample 2xx, keep all 4xx/5xx.

## 4. Grafana Cloud Adaptive Logs
Analyses patterns and recommends per-pattern drop rates; applied server-side before storage. Review
recommendations, exempt patterns you alert on (`Exemptions`), and watch "dropped volume" afterwards.

## 5. Shorten retention for noisy tenants/streams
Loki `retention_stream` per selector: `{namespace="dev"}` 7d while prod is 30d.

## Guardrails
- Never sample audit or security logs.
- Keep counters for anything dropped that you alert on (log-derived metric before the drop).
- Record the sample rate as a label/field so counts can be re-weighted.

## Verify
Compare `loki_distributor_bytes_received_total` (or billing) before and after over a full weekly cycle.
