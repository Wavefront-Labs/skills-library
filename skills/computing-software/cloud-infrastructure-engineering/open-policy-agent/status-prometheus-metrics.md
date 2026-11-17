---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.status-prometheus-metrics
name: status-prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [prometheus, bundle-metrics, decision-log-metrics, alerting, status-plugin]
level: advanced
status: docs-checked
description: "Alert on OPA bundle and decision log health with the status plugin's Prometheus metrics: bundle load counters, last-success gauges and dropped-decision counters."
sources:
  - https://www.openpolicyagent.org/docs/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: alert on stale bundles and lost decision logs from Prometheus.

When Prometheus is enabled in the status plugin, OPA's Prometheus endpoint exposes extra metrics beyond the Go and HTTP ones.

Bundles:
- `bundle_loaded_counter`, `bundle_failed_load_counter`
- `last_bundle_request`, `last_success_bundle_request`, `last_success_bundle_download`, `last_success_bundle_activation` (UNIX nanoseconds)
- `bundle_loading_duration_ns` histogram
- `plugin_status_gauge`: plugins by name and status; `opa_info` for environment info

Decision logs:
- `decision_logs_status_gauge`: last upload outcome, labelled `code` and `http_code` (both empty on success)
- `decision_logs_dropped_rate_limit_exceeded_total`: dropped past `decision_logs.reporting.max_decisions_per_second`
- `decision_logs_dropped_buffer_size_limit_exceeded_total` and `..._bytes_exceeded_total`: dropped because a buffer was full
- `decision_logs_encoding_failure_total`: could not be encoded or did not fit `upload_size_limit_bytes`
- `decision_logs_nd_builtin_cache_dropped_total`: logged without the non-deterministic builtin cache
- experimental: `decision_logs_chunks_uploaded_total`, `decision_logs_chunks_upload_failed_total` (failed chunks are requeued), `decision_logs_buffer_size_events`, `decision_logs_buffer_size_bytes`

The `decision_logs_*` and `enc_*` counters update with each status update and are exported only after the decision logs plugin has reported them. The buffer gauges are read at scrape time, and only the one matching `decision_logs.reporting.buffer_type` is exported.

Useful alerts: `bundle_failed_load_counter` increasing, time since `last_success_bundle_activation` beyond your polling interval, and any increase of the dropped counters.

Check: break the bundle URL and confirm `bundle_failed_load_counter` rises at the next poll.

## Checked

Metric names, types and the export conditions were confirmed in the Status Metrics section of the Monitoring page. The suggested alerts are practice advice, not from the page.

Method: docs-checked 2026-11-09 against the OPA docs monitoring page (docs/docs/monitoring.md in the OPA repository, full file read).
