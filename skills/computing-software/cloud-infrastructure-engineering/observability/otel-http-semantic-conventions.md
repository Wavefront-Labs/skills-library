---
id: computing-software.cloud-infrastructure-engineering.observability.otel-http-semantic-conventions
name: otel-http-semantic-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [http-semantic-conventions, http-server-attributes, semantic-conventions, http-route, span-naming]
level: practitioner
status: docs-checked
description: "Apply stable OTel HTTP semantic conventions: span names, required server/client attributes, status rules, http.server.request.duration metric and bucket boundaries."
sources: ["https://opentelemetry.io/docs/specs/semconv/http/http-spans/", "https://opentelemetry.io/docs/specs/semconv/http/http-metrics/", "https://opentelemetry.io/docs/specs/semconv/registry/attributes/http/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP semantic conventions (stable)

The HTTP span and metric conventions are marked Stable in the semantic conventions repository (some attributes and metrics noted below are still Development). Hand-written spans should follow them so dashboards and backends (span metrics, service graphs) work.

## Span name
`{method} {target}` when a low-cardinality target exists, otherwise `{method}`. Server: `{http.request.method} {http.route}` ->
`GET /orders/{id}`. Client: `{http.request.method}`, with `url.template` as target only if enabled and available (Development).
Instrumentation MUST NOT default to the URI path as target. When the method is `_OTHER` the span name uses `HTTP`; the original
method goes in `http.request.method_original`.

## Server span attributes
| Attribute | Requirement |
|---|---|
| `http.request.method` | required |
| `url.path`, `url.scheme` | required |
| `http.route` | conditionally required (if available) |
| `http.response.status_code` | conditionally required (if one was sent) |
| `error.type` | conditionally required (if the request ended with an error; status code as string or exception type) |
| `server.port` | conditionally required (if available and `server.address` is set) |
| `url.query` | conditionally required (if one was received) |
| `server.address`, `client.address`, `user_agent.original`, `network.protocol.version` | recommended |

## Client span attributes
Required: `http.request.method`, `url.full`, `server.address`, `server.port`. Conditionally required: `http.response.status_code`
(if received) and `error.type` (if the request ended with an error). Recommended: `http.request.resend_count` (only if retried),
`network.protocol.version`. `url.full` MUST NOT contain credentials; the spec says to redact them as
`https://REDACTED:REDACTED@host/`.

## Status
- Status is left unset for success codes. For 4xx the status MUST stay unset on server spans and SHOULD be Error on client spans.
  For 5xx (and codes the client could not interpret) it SHOULD be Error. Do not set a description that can be inferred from
  `http.response.status_code`.

## Metrics
`http.server.request.duration` and `http.client.request.duration` (Stable): histogram, unit `s`; the server metric SHOULD use the
`ExplicitBucketBoundaries` advisory `[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10]`. Server attributes:
`http.request.method`, `url.scheme` (required), `http.route` and `http.response.status_code` (conditionally required), `error.type`
(conditionally required), `network.protocol.version` (recommended), `server.address` (opt-in).
Currently Development: `http.server.active_requests` (UpDownCounter, `{request}`) and the `*.body.size` histograms (unit `By`).

## Gotchas
- Route must be set before the span ends; frameworks that resolve routes late may need a span name update.
- Capturing headers is opt-in (`http.request.header.<name>`); allowlist, never capture auth headers.

## Checked

2026-10-24. OpenTelemetry semantic conventions repository docs/http/http-spans.md and http-metrics.md (main branch). Confirmed: span naming rules including `_OTHER` and `HTTP`, requirement levels for server and client span attributes, status rules for 4xx and 5xx, `url.full` credential redaction, metric names, units, bucket advisory, server metric attributes, and Development stability of active_requests and body size metrics. Corrected: client `url.full`, `server.address` and `server.port` are Required; server `server.port` and `url.query` are conditionally required; `url.scheme` is not required on client spans. Removed the Prometheus name-mapping line and the stabilisation date.

Method: documentation only; no commands were run.
