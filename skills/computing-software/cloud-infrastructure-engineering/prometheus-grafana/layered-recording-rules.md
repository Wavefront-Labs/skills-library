---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.layered-recording-rules
name: layered-recording-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [layered-recording-rules, aggregation-hierarchy, recording-rules, recording-rule-naming, rule-performance]
level: practitioner
status: verified
description: "Build recording rules in layers (instance to job to cluster to global) using level:metric:operations naming, so dashboards and alerts query small pre-aggregated series."
sources: ["https://prometheus.io/docs/practices/rules/", "https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/", "https://monitoring.mixins.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layered recording rules

prometheus.io rules practice: name as `level:metric:operations`; aggregate in steps so each layer reads the previous layer, not raw data.

## Example hierarchy
```yaml
groups:
  - name: http-layers
    interval: 30s
    rules:
      # layer 1: per instance rate (removes nothing but computes rate once)
      - record: instance_path:http_requests:rate5m
        expr: sum without (method) (rate(http_requests_total[5m]))
      # layer 2: per job/path from layer 1
      - record: job_path:http_requests:rate5m
        expr: sum without (instance) (instance_path:http_requests:rate5m)
      # layer 3: per job
      - record: job:http_requests:rate5m
        expr: sum without (path) (job_path:http_requests:rate5m)
```
Rules in one group evaluate sequentially in order, so later rules read the current evaluation's outputs (tested with `promtool test rules`: `job:http_requests:rate5m` equalled `sum(rate(http_requests_total[5m]))` at the same time).

## Ratios
Record numerator and denominator separately at each layer and divide at the top, never average lower-layer ratios:
```yaml
- record: job:http_request_errors:ratio_rate5m
  expr: job:http_request_errors:rate5m / job:http_requests:rate5m
```

## Benefits
- Dashboards over 30 days read thousands of series instead of millions.
- Federation and remote write of top layers only.
- Consistent definitions shared by alerts and dashboards.

## Gotchas
- Keep dependent rules in the same group: Prometheus docs say rules in a group run sequentially with the same evaluation time, so do not rely on ordering across groups.
- `without` in lower layers keeps target labels like `cluster` for upper layers; `by` lists must include them.
- Changing a lower layer's labels breaks upper layers silently; unit test the chain with promtool.

## Verify
- [ ] Top-layer series value equals the raw-query value at a sample time (promql_expr_test).
