---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.info-and-enum-metric-patterns
name: info-and-enum-metric-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [info-metrics-pattern, enum-metrics, stateset-info, group-left, target-info, data-model]
level: practitioner
status: verified
description: "Expose metadata as *_info metrics and states as enum/stateset series, then join them in PromQL with group_left or the experimental info() function."
sources: ["https://prometheus.io/docs/practices/naming/", "https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md", "https://prometheus.io/docs/prometheus/latest/querying/functions/#info"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Info and enum metric patterns

## Info metrics
Value always 1; labels carry metadata that would otherwise repeat on every series.
```
app_build_info{version="1.8.2",revision="a1b2c3",goversion="go1.23"} 1
```
Join to add `version` to a request rate:
```promql
sum by (instance, version) (
  rate(http_requests_total[5m])
  * on (instance) group_left (version) app_build_info
)
```
OTel resource attributes arrive as `target_info{job, instance, ...}`. Prometheus 3.x experimental `info()` (needs `--enable-feature=promql-experimental-functions`; without it the parser says `function "info" is not enabled`) does the join for `target_info`:
```promql
info(rate(http_server_request_duration_seconds_count[5m]), {k8s_cluster_name=~".+"})
```

## Enum (state) metrics
One series per possible state, value 1 for the current state, 0 for others:
```
service_state{state="starting"} 0
service_state{state="running"} 1
service_state{state="degraded"} 0
```
OpenMetrics calls this a StateSet. Query current state: `service_state == 1`. Time in state: `avg_over_time(service_state{state="degraded"}[1d])` = fraction of the day.
Avoid encoding states as numbers (`state=2`): unreadable and `avg` produces meaningless 1.5.

## Rules
- Info label values must be bounded (versions are fine, request ids are not).
- When an info label changes (deploy), the old series goes stale and a new one starts; joins briefly see both and fail with `found duplicate series for the match group {instance="i1"} on the right hand-side of the operation ... many-to-many matching not allowed`. Pick one series per instance with `topk by (instance) (1, app_build_info)` as the right-hand side (it keeps the `version` label); `max by (instance) (app_build_info)` also removes the duplicate but drops `version`, so it cannot supply that label.
- Do not put info labels directly onto every metric in the app.

## Verify
- [ ] `count by (instance) (app_build_info) > 1` is empty outside deploy windows.
- [ ] Each enum metric always has exactly one state at 1 per instance.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26.
- promtool tests with two `app_build_info` series (versions 1.8.1 and 1.8.2) for one instance: the skill's join raised the many-to-many error above; with `topk by (instance) (1, app_build_info)` on the right it returned `{instance="i1", version="1.8.2"} 1`; `max by (instance)` returned one series without `version`. `svc_state == 1` returned the running and degraded series that were 1; `avg_over_time(svc_state{state="degraded"}[10m])` returned 0.6 for a state that was 1 for 6 of 10 samples.
- `info()`: the skill's example form `info(rate(req_count_total[1m]), {k8s_cluster_name=~".+"})` returned the series with `k8s_cluster_name="c1"` joined from `target_info` on a 3.15.1 server started with `--enable-feature=promql-experimental-functions`; promtool's test engine still answered `function "info" is not enabled` with that flag, so test it on a server. The experimental status of `info` is stated in the 3.15 functions page.
- `target_info` produced by the OTLP receiver: see `otel-to-prometheus-metric-name-translation`. StateSet and info types: OpenMetrics specification (see `openmetrics-features`).
