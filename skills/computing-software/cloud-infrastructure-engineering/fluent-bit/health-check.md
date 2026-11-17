---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.health-check
name: health-check
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, health-check, hc-errors-count, hc-retry-failure-count, hc-period, kubernetes-probes]
level: practitioner
status: docs-checked
description: "Configure Fluent Bit's health endpoint so errors and retry failures over a period report unhealthy with HTTP 500."
sources: ["https://docs.fluentbit.io/manual/administration/monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Health check

Health checking needs the HTTP server and `health_check: on` (default off).

| Key | Default | Meaning |
| --- | --- | --- |
| `hc_errors_count` | `5` | output error count that makes Fluent Bit unhealthy |
| `hc_retry_failure_count` | `5` | retry failure count that makes it unhealthy |
| `hc_period` | `60` | seconds over which errors and retry failures are counted |

Both counts are sums across all output plugins within the period. Fluent Bit is unhealthy when errors exceed `hc_errors_count` or retry failures exceed `hc_retry_failure_count` inside `hc_period`. Not every error log counts: only the failed-flush and cannot-be-retried warnings from the engine do.

```yaml
service:
  http_server: on
  http_listen: 0.0.0.0
  http_port: 2020
  health_check: on
  hc_errors_count: 5
  hc_retry_failure_count: 5
  hc_period: 5
```

`/api/v1/health` returns `ok` with HTTP 200 or `error` with HTTP 500. `/api/v2/health` returns JSON with `status`, `errors`, `retries_failed`, `error_limit`, `retry_failure_limit` and `period_limit`.

Call the endpoint with `curl -s http://127.0.0.1:2020/api/v2/health`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Monitoring page (Health check for Fluent Bit and the endpoint list): Health_Check, HC_Errors_Count, HC_Retry_Failure_Count, HC_Period and defaults, sum across outputs, 200 and 500 behaviour, v2 response fields, the example configuration. Removed: unsourced probe advice.

Method: documentation only; no commands were run.
