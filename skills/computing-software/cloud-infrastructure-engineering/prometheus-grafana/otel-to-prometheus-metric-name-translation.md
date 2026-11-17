---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.otel-to-prometheus-metric-name-translation
name: otel-to-prometheus-metric-name-translation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [otel-prometheus-name-translation, translation-strategy, otlp, prometheus-otlp-receiver, utf8-metric-names, target-info]
level: advanced
status: verified
description: "How OTLP metric names, units and resource attributes map to Prometheus names (suffixes, underscores, target_info) and how translation_strategy changes it."
sources: ["https://prometheus.io/docs/guides/opentelemetry/", "https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/compatibility/prometheus_and_openmetrics.md", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#otlp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTel to Prometheus name translation

## Default mapping (spec "Prometheus and OpenMetrics compatibility")
| OTel | Prometheus |
|---|---|
| `http.server.request.duration` unit `s`, histogram | `http_server_request_duration_seconds_bucket/_sum/_count` |
| counter `requests` unit `1` (monotonic sum) | `requests_total` |
| gauge `cpu.utilization` unit `1` | `cpu_utilization_ratio` |
| unit `By` / `ms` / `{request}` | `_bytes` / `_milliseconds` / (annotation units in braces dropped) |
| attribute `http.response.status_code` | label `http_response_status_code` |
| resource attributes | `target_info` series; `service.name` (+namespace) to `job`, `service.instance.id` to `instance` |

## Prometheus OTLP receiver (`--web.enable-otlp-receiver`)
```yaml
otlp:
  translation_strategy: UnderscoreEscapingWithSuffixes   # default; others: UnderscoreEscapingWithoutSuffixes, NoUTF8EscapingWithSuffixes, NoTranslation (experimental)
  promote_resource_attributes: [service.namespace, k8s.namespace.name, k8s.pod.name]
  keep_identifying_resource_attributes: true
```
- With UTF-8 strategies names keep dots: query with `{"http.server.request.duration_seconds_bucket"}` style quoting. Results for the same payload: `NoUTF8EscapingWithSuffixes` gave `http.server.request.duration_seconds_bucket`, `cpu.utilization_ratio`, `mem.used_bytes`; `UnderscoreEscapingWithoutSuffixes` gave `http_server_request_duration_bucket`, `cpu_utilization`; `NoTranslation` gave `http.server.request.duration_bucket`, `cpu.utilization`, `requests`.
- Promoted resource attributes become labels on every series (cardinality!); the rest stay only on `target_info`.

## Collector prometheus/prometheusremotewrite exporters
Their READMEs now steer to `translation_strategy` (replacing `add_metric_suffixes`) and `resource_constant_labels` (replacing `resource_to_telemetry_conversion`, which copied all resource attributes to labels: usually too many); check the README of your collector version.

## Gotchas
- Switching strategies renames every metric; dashboards and rules break. Decide once, early.
- Two OTel metrics differing only by `.` vs `_` collide after underscore escaping.
- Delta temporality: by default the receiver refuses a request containing a delta counter (`500 invalid temporality and type combination for metric "delta.counter"`, the whole request fails). Convert with the collector's `deltatocumulative` processor or start Prometheus with `--enable-feature=otlp-deltatocumulative` (two deltas of 2 became a cumulative 4); the state is in memory, so a Prometheus restart shows a counter reset.

## Verify
- [ ] Names in Prometheus match what dashboards expect (`count by (__name__) ({job="svc"})`).
- [ ] `target_info` exists for each service and joins with `on (job, instance)`.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26; OTLP JSON posted to `/api/v1/otlp/v1/metrics` of a server started with `--web.enable-otlp-receiver`.
- Payload: histogram `http.server.request.duration` (unit `s`, attribute `http.response.status_code`), monotonic cumulative sum `requests` (unit `1`), gauges `cpu.utilization` (`1`), `mem.used` (`By`), `lat` (`ms`), `inflight` (`{request}`), resource attributes `service.name`, `service.namespace`, `service.instance.id`, `k8s.pod.name`. With the default strategy the stored names were `http_server_request_duration_seconds_bucket/_count/_sum`, `requests_total`, `cpu_utilization_ratio`, `mem_used_bytes`, `lat_milliseconds`, `inflight` (no suffix for the braces unit), the label `http_response_status_code`, and `target_info` with `job="ns/svc"`, `instance="inst1"`, `service_name`, `service_namespace`, `service_instance_id` (keep_identifying_resource_attributes true) and the promoted `k8s_pod_name`. The other three strategies produced the name sets given above.
- A delta-temporality counter in the payload made the request fail with the message above; with `--enable-feature=otlp-deltatocumulative` two posts of delta 2 queried as `delta_counter_total 4`.
- Strategy names and keys (`promote_resource_attributes`, `keep_identifying_resource_attributes`): 3.15 configuration page. Collector exporter README notes: opentelemetry-collector-contrib `prometheusremotewriteexporter` and `prometheusexporter`. The OTel specification page named in `sources` was not re-fetched; the mapping above was checked by running the receiver.
