---
id: computing-software.cloud-infrastructure-engineering.cortex.query-tee
name: query-tee
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [query-tee, comparison, backends, migration, performance]
level: practitioner
status: docs-checked
description: "Compare read performance and responses of two or more Cortex backends with the query-tee proxy."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/query-tee.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The query-tee is a standalone service for testing. It exposes Prometheus-compatible read endpoints, sends each request to all configured backends, records each backend's response time and returns one of the responses to the client. Use it to compare backends, such as two Cortex clusters ingesting the same series.

Run it from source (`go run ./cmd/query-tee -help`) or the image `quay.io/cortexproject/query-tee`. At least one backend is required, two to compare, passed as comma-separated URLs in `-backend.endpoints`.

Supported GET endpoints: `/api/v1/query`, `/api/v1/query_range`, `/api/v1/labels`, `/api/v1/label/{name}/values`, `/api/v1/series`, `/api/v1/metadata`, `/api/v1/alerts` and `/api/v1/rules`.

Pass-through: with `-proxy.passthrough-non-registered-routes=true` and a preferred backend configured, requests to routes not in the list go only to the preferred backend, making it a transparent proxy for everything else.

Response selection: set a preferred backend with `-backend.preferred=` (its hostname). The preferred backend's response is returned if its status is 2xx or 4xx; otherwise the first received 2xx or 4xx response, otherwise the first received response. A 4xx counts as success because it usually means an invalid request. Without a preferred backend the same first-2xx-or-4xx rule applies. The first viable response is returned without waiting for slow backends.

Comparison: `-proxy.compare-responses=true` requires exactly two backends with a preferred one, logs each query whose results differ and counts outcomes in `cortex_querytee_responses_compared_total`. Floating point values are compared with a tolerance set by `-proxy.value-comparison-tolerance`. Metrics are served on the port from `-server.metrics-port`.

HTTP basic authentication: a backend URL with username and password uses them; a URL with only a username keeps it and injects the password from the incoming request; a URL with neither forwards the incoming request's basic auth.

## Checked

Method: docs-checked 2026-11-09 against the Cortex query-tee page (raw markdown, read in full). A pointer to the query auditor in the troubleshooting guide was dropped as unconfirmed.
