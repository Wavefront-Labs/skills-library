---
id: computing-software.cloud-infrastructure-engineering.harbor.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [metrics, prometheus, exporter, harbor-core-metrics, harbor]
level: practitioner
status: docs-checked
description: "Expose Harbor metrics and scrape the exporter, core, registry and jobservice endpoints, with the key metric names and labels."
sources:
  - https://goharbor.io/docs/main/administration/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable metrics in the Harbor configuration file (v2.2 and later). They are served at `<harbor_instance>:<metrics_port>/<metrics_path>`; the exporter is the default target, and other components are selected with a query parameter:
- `?comp=core`: `harbor_core_http_inflight_requests`, `harbor_core_http_request_duration_seconds`, `harbor_core_http_request_total`, labelled by method and operation (the `operationId` from the Harbor API swagger).
- `?comp=registry`: `registry_http_in_flight_requests`, `registry_http_requests_total` (code, handler, method), `registry_http_request_duration_seconds_*`, `registry_storage_action_seconds_*`, `registry_storage_cache_total`.
- `?comp=jobservice`: `harbor_jobservice_info`, `harbor_jobservice_task_total` (instance, job, status, type).

Exporter metrics (no parameter) come from configuration and the database:
- `harbor_project_total`, `harbor_project_repo_total`, `harbor_project_member_total`, `harbor_project_artifact_total`
- `harbor_project_quota_usage_byte` and `harbor_project_quota_byte` per project_name
- `harbor_artifact_pulled`
- `harbor_health`, and `harbor_up` with component label (`core`, `database`, `jobservice`, `portal`, `redis`, `registry`, `registryctl`, `trivy`)
- `harbor_system_info` with auth_mode, harbor_version and self_registration
- `harbor_task_queue_size`, `harbor_task_queue_latency`, `harbor_task_scheduled_total`, `harbor_task_concurrency`

Also exposed: Go runtime data, request counts in flight in core, and Distribution notification metrics.

The exporter component serves metrics without a query parameter; core, registry and jobservice each need their own `comp` value, so configure one scrape job per component.

In `harbor.yml`, enable the endpoint with the `metric` block: `enabled` (default false), `port` (default 9090) and `path` (default /metrics).

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Access Metrics and the YML file page.
Method: documentation only; no commands were run.
