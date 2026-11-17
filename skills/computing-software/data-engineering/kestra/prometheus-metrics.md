---
id: computing-software.data-engineering.kestra.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: data-engineering
product: kestra
tags: [prometheus, metrics, port-8081, queue-lag, monitoring, micrometer]
level: practitioner
status: docs-checked
description: "Scrape Kestra Prometheus metrics from port 8081, the main metric families per server component, and enabling the queue lag metric."
sources:
  - https://kestra.io/docs/administrator-guide/prometheus-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prometheus metrics are enabled by default and served at `http://localhost:8081/prometheus`. OpenTelemetry, by contrast, must be explicitly enabled in the configuration file. Metrics include custom metrics defined in the application and framework metrics collected via Micrometer.

Families:

- Executor (executor server exclusive): `kestra_executor_execution_started_count_total`, `kestra_executor_execution_queued_count_total`, `kestra_executor_execution_end_count_total`, `kestra_executor_sla_violation_count_total`.
- Scheduler (scheduler server exclusive): `kestra_scheduler_trigger_count_total`, `kestra_scheduler_trigger_delay_duration_seconds` (delay between a trigger's scheduled date and its evaluation; backfills are excluded).
- Worker: `kestra_worker_running_count`, `kestra_worker_pending_count`, `kestra_worker_timeout_count_total`. Every worker metric except `kestra_worker_killed_count_total` is tagged with `worker_group`.
- Worker controller (worker controller server exclusive): `kestra_controller_job_dispatched_total`, `kestra_controller_job_inflight`.
- Queue: `kestra_queue_message_emitted_total`, `kestra_queue_message_lag`.
- Database: `kestra_jdbc_query_duration_seconds`, plus HikariCP pool metrics named `hikaricp_connections*`.
- Indexer: `kestra_indexer_message_in_count_total`, `kestra_indexer_request_duration_seconds`; emitted by every server that runs an indexer, including webserver and standalone servers.
- HTTP server metrics such as `http_server_requests_seconds`, plus cache and JVM metrics listed on the page.

`kestra_queue_message_lag` (worker jobs not yet consumed, tagged by `worker_queue`) is reported by the webserver or standalone server only when `kestra.metric.queue.lag.enabled` is true.

Notes:

- `kestra_executor_quota_exceeded_total` is Enterprise Edition.
- Each `_seconds` summary has a companion `_max` gauge.

## Checked

2026-11-04. Confirmed against "Available Prometheus metrics and how to scrape them" (administrator-guide/prometheus-metrics): default enablement, endpoint, every metric name above, exclusivity notes, worker_group tagging, queue lag condition, Enterprise note, `_max` gauges. Removed: the example config line form for the lag setting (page only says it must be true) and a claim that the metrics are only "counters and gauges".
Method: documentation only; no commands were run.
