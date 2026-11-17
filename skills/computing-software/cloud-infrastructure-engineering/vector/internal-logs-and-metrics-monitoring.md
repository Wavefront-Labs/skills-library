---
id: computing-software.cloud-infrastructure-engineering.vector.internal-logs-and-metrics-monitoring
name: internal-logs-and-metrics-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [monitoring, internal-logs, internal-metrics, log-level, prometheus, observability, vector]
level: practitioner
status: docs-checked
description: "Observe Vector with its internal_logs and internal_metrics sources and set log levels."
sources:
  - https://vector.dev/docs/administration/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vector exposes its own telemetry as sources you route like any other data.

Logs: the `internal_logs` source (default level info). Vector also writes logs to stderr for systemd or Kubernetes to capture.

```yaml
sources:
  vector_logs:
    type: internal_logs
sinks:
  console:
    type: console
    inputs: [vector_logs]
    encoding: {codec: text}
```

Metrics: the `internal_metrics` source, for example into Prometheus remote write:

```yaml
sources:
  vector_metrics:
    type: internal_metrics
sinks:
  prometheus:
    type: prometheus_remote_write
    endpoint: https://localhost:8087/
    inputs: [vector_metrics]
```

Log levels: `-v` gives debug, `-vv` trace, `-q` warn, `-qq` error, `-qqq` off; or `VECTOR_LOG=<level>` with trace, debug, info, warn, error or off. `RUST_BACKTRACE=full` gives full error backtraces.

Rate limiting: Vector limits repeated log events in the hot path to avoid saturating IO, so repetitive messages are suppressed.

## Checked

Method: docs-checked 2026-11-09 against the full Vector monitoring page (raw markdown from the vectordotdev/vector repo). Dropped the rate-limit flag names and defaults, which are not on that page, and an unsourced verification line.
