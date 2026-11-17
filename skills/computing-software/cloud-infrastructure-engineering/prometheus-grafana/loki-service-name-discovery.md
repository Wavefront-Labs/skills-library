---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-service-name-discovery
name: loki-service-name-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [discover-service-name, service-name-label, loki-labels, otlp-attribute-mapping-loki, discover-log-levels]
level: practitioner
status: verified
description: "How Loki 3 derives the service_name label (discover_service_name list, OTLP service.name, unknown_service) and detected_level, and how to tune or disable it."
sources: ["https://grafana.com/docs/loki/latest/get-started/labels/#default-labels-for-all-users", "https://grafana.com/docs/loki/latest/configure/#limits_config", "https://grafana.com/docs/grafana/latest/explore/simplified-exploration/logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki service_name discovery

Loki 3 ensures every stream has a `service_name` label (used by Grafana Logs Drilldown).

## Rules
- OTLP ingestion: `service.name` resource attribute becomes `service_name`.
- Otherwise the distributor looks for the first present label from `limits_config.discover_service_name`, by default (Loki 3.7.9, from `-print-config-stderr`) `service, app, application, app_name, name, app_kubernetes_io_name, container, container_name, k8s_container_name, component, workload, job, k8s_job_name`, and copies its value. A stream that already has `service_name` keeps it (upgrade guide).
- If nothing matches: `service_name="unknown_service"`.

```yaml
limits_config:
  discover_service_name: [app_kubernetes_io_name, app, container, job]
  discover_log_levels: true         # default true; adds detected_level structured metadata (seen as `detected_level` on JSON, logfmt and OTLP lines)
```
Set `discover_service_name: []` to disable.

## Recommendations
- Set `service_name` explicitly in the agent (Alloy relabel from `app.kubernetes.io/name`) so it does not depend on fallback order.
- Keep values aligned with `service.name` in traces and metrics for correlation.

## Gotchas
- After upgrading to 3.x, a new label appears on all streams; queries comparing exact label sets or recording rules grouping `by (all labels)` may change.
- `unknown_service` streams are a to-do list: fix the agent labels.

## Verify
- [ ] `count by (service_name) (count_over_time({service_name=~".+"}[5m]))` shows meaningful names, few unknown_service.

## Checked
Ran Loki 3.7.9 (local): a stream labelled only `app="api"` got `service_name="api"`; with `discover_service_name: [app_kubernetes_io_name, app, container, job]` set it still resolved from `app`; a stream with only unrelated labels got `service_name="unknown_service"` (visible in the rejection message of an over-wide label set); OTLP `service.name=checkout` became `service_name="checkout"`; `detected_level` appeared on JSON, logfmt and OTLP entries; `count by (service_name) (count_over_time({service_name=~".+"}[5m]))` returned the series. Default list read from `-print-config-stderr` and the v3.7.9 configuration reference; the empty-list disable and the already-has-`service_name` rule are from the upgrade guide (docs/sources/setup/upgrade). The plugin name Grafana Logs Drilldown was read from the bundled `grafana-lokiexplore-app` plugin.json in Grafana 13.2.4.
