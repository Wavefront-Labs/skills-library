---
id: computing-software.cloud-infrastructure-engineering.observability.log-schema-and-field-naming
name: log-schema-and-field-naming
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-schema-design, field-naming, structured-logging, semantic-conventions, ecs]
level: practitioner
status: draft
description: "Design a structured log schema: required fields, naming style, types, OTel semantic convention and ECS alignment, and enforcing the schema across services."
sources: ["https://opentelemetry.io/docs/specs/otel/logs/data-model/", "https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/", "https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log schema and field naming

## Pick one convention and document it
Prefer OTel semantic conventions (dot-namespaced, lowercase, snake_case words: `http.request.method`,
`user.id`, `exception.stacktrace`). If you are on Elastic, ECS uses the same dotted style and largely aligns
(ECS and OTel semconv are converging). Never mix `userId`, `user_id` and `uid` across services.

## Required fields (every line)
| Field | Example | Note |
|---|---|---|
| `timestamp` | `2026-10-16T09:12:03.123Z` | RFC 3339 UTC with ms |
| `severity_text` / `level` | `INFO` | fixed set |
| `message` / `body` | `payment declined` | constant template, no variables |
| `service.name`, `service.version` | `checkout`, `1.42.0` | |
| `deployment.environment.name` | `prod` | |
| `trace_id`, `span_id` | 32/16 hex | when in a request |

## Contextual fields
`http.request.method`, `http.route`, `http.response.status_code`, `url.path`, `user.id` (hashed if needed),
`error.type`, `exception.type`, `exception.message`, `exception.stacktrace`, `event.name`, `duration_ms`.

## Rules
- Types are stable: a field is always a number or always a string (Elasticsearch mapping conflicts and
  Loki `| json` comparisons break otherwise).
- Units in the name when not obvious (`duration_ms`, `size_bytes`).
- Custom fields under your own namespace (`acme.order.id`), not top level.
- No dynamic keys (`"user_123": {...}`) - they explode index mappings.
- Keep the message human-readable and stable; variables go in fields.

## Enforcement
- Shared logging library/config per language (Logback JSON encoder, structlog processor chain, zap encoder
  config) that adds required fields.
- CI check: unit test that parses a sample line and validates against a JSON Schema.
- Ingest-side normalisation (OTel `transform`/Alloy) for legacy services rather than per-team mapping in queries.

## Example
```json
{"timestamp":"2026-10-16T09:12:03.123Z","level":"WARN","message":"payment declined",
 "service.name":"checkout","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7",
 "acme.order.id":"o-991","error.type":"insufficient_funds","duration_ms":182}
```
