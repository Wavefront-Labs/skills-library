---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.monitoring-endpoints
name: monitoring-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, monitoring, http-server, prometheus, metrics-endpoint, api-v1, api-v2]
level: practitioner
status: docs-checked
description: "Enable Fluent Bit's built-in HTTP server and pick the right monitoring endpoint for JSON, Prometheus or health data."
sources: ["https://docs.fluentbit.io/manual/administration/monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring endpoints

Enable the built-in HTTP server in the service section:

```yaml
service:
  http_server: on
  http_listen: 0.0.0.0
  http_port: 2020
```

Then query it, for example `curl -s http://127.0.0.1:2020 | jq`. Endpoints:

| URI | Returns |
| --- | --- |
| `/` | build information, JSON |
| `/api/v1/uptime` | uptime in seconds, JSON |
| `/api/v1/metrics` | per-plugin internal metrics, JSON |
| `/api/v1/metrics/prometheus` | the same in Prometheus text 0.0.4 |
| `/api/v1/storage` | storage layer and buffered data; only when `storage.metrics` is on |
| `/api/v1/health` | health result as a string |
| `/api/v2/metrics` | per-plugin metrics in cmetrics text format |
| `/api/v2/metrics/prometheus` | Prometheus text 0.0.4 |
| `/api/v2/health` | health as JSON: 200 healthy, 500 unhealthy |
| `/api/v2/reload` | hot reload (`POST`, `PUT`) or status of hot reloading (`GET`); other methods return 405 |

The v2 Prometheus endpoint serves the cmetrics-based metrics in Prometheus text format; the v1 endpoints are the older per-plugin metrics. In Fluent Bit 5.1 and later, an HTTP server that cannot start (for example, the port is in use) is a startup failure: Fluent Bit logs `could not start HTTP server` and exits.

The health and reload endpoints are described in `computing-software.cloud-infrastructure-engineering.fluent-bit.health-check` and `computing-software.cloud-infrastructure-engineering.fluent-bit.hot-reload`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs monitoring page (raw markdown; HTTP server, REST API table and health sections read).
