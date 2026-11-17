---
id: computing-software.cloud-infrastructure-engineering.garage.health-endpoint-and-metrics-access
name: health-endpoint-and-metrics-access
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [health-endpoint, metrics-require-token, prometheus-metrics, admin-endpoint]
level: practitioner
status: docs-checked
description: "Use the unauthenticated /health check and secure /metrics with metrics_token or metrics_require_token."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/admin-api/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The admin server exposes a health check at `GET /health`. It returns 200 OK when enough nodes are up to hold a quorum and serve requests, and 503 Service Unavailable otherwise.

The Prometheus endpoint is `/metrics`, for example `curl -i http://localhost:3903/metrics`, returning `text/plain; version=0.0.4`.

Access control for metrics:

- `metrics_token` (or `metrics_token_file`, or `GARAGE_METRICS_TOKEN`, `GARAGE_METRICS_TOKEN_FILE`) protects the endpoint. If it is unset and `metrics_require_token` is not true, anyone who can reach the admin port can read metrics.
- `metrics_require_token` (since v2.0.0): when true, a token is always required. Valid tokens are the `metrics_token`, if set, and dynamic admin tokens whose scope includes the Metrics endpoint.

The token list shows the config token as `metrics_token (from daemon configuration)` with scope `Metrics`.

## Checked

2026-11-04. Read the Administration API and Configuration file format pages in full. Confirmed the /health responses, the /metrics example and content type, the metrics token options, the metrics_require_token behaviour and the token list line. Removed the load balancer remark and the Prometheus scrape configuration, which these pages do not state.
Method: documentation only; no commands were run.
