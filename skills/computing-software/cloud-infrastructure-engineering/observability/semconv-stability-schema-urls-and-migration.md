---
id: computing-software.cloud-infrastructure-engineering.observability.semconv-stability-schema-urls-and-migration
name: semconv-stability-schema-urls-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [semconv-stability, schema-url, http-semconv-migration, semantic-conventions, otel-semconv-stability-opt-in]
level: advanced
status: docs-checked
description: "Handle semantic convention versions: stability levels, schema URLs, OTEL_SEMCONV_STABILITY_OPT_IN dual emission, old to new HTTP names, and migrating dashboards and alerts."
sources: ["https://opentelemetry.io/docs/specs/semconv/http/migration-guide/", "https://opentelemetry.io/docs/specs/otel/schemas/", "https://opentelemetry.io/docs/specs/otel/versioning-and-stability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semconv stability, schema URLs and migration

## Stability levels
Development (experimental) -> Release Candidate -> Stable. Only stable conventions are guaranteed not to change
names. HTTP and database conventions have stable opt-in values (`http`, `database`) in `OTEL_SEMCONV_STABILITY_OPT_IN`; check the Stability column on each semconv page for the rest.

## Schema URL
Telemetry carries the semconv version it follows: `schema_url: https://opentelemetry.io/schemas/1.26.0` on Resource
and InstrumentationScope. Schema files describe renames between versions so backends/collectors can translate; the schemas spec describes a Collector "Schema Translate Processor" for this.

## Opt-in during a breaking rename
`OTEL_SEMCONV_STABILITY_OPT_IN` (comma list of category values such as `http`, `database`): `http` emits only the stable names, `http/dup` emits both old and new. The spec says the variable is only for migrating from an experimental convention to its first stable version. Use `/dup` for a transition window, then switch.

## HTTP old -> new (the big one)
| Old | New |
|---|---|
| `http.method` | `http.request.method` |
| `http.status_code` | `http.response.status_code` |
| `http.url` | `url.full` |
| `http.target` | `url.path` + `url.query` |
| `http.scheme` | `url.scheme` |
| `net.peer.name` / `net.host.name` | `server.address` |
| `net.sock.peer.addr` | `network.peer.address` |
| `http.user_agent` | `user_agent.original` |
| metric `http.server.duration` (ms) | `http.server.request.duration` (**s**) |

## Migration plan
1. Inventory consumers: dashboards, alerts, recording rules, SLOs, TraceQL saved queries using old names.
2. Enable `/dup` in instrumentation (cost: more attributes, two metric families).
3. Update consumers to new names; for metrics note the unit change (multiply thresholds by 0.001).
4. Switch to new-only; remove dual.
Alternative for mixed estates: normalise in the collector with OTTL
`set(attributes["http.request.method"], attributes["http.method"]) where attributes["http.method"] != nil` then delete old.

## Gotchas
- Upgrading an agent or SDK can change which semconv version it emits by default; read its release notes before upgrading.

## Checked
- 2026-10-28. Checked against the semconv HTTP migration guide, the OpenTelemetry schemas spec, the versioning-and-stability page, the 1.26.0 schema file and the SDK/language docs for `OTEL_SEMCONV_STABILITY_OPT_IN` (semconv docs as served 2026-10).
- Confirmed: `http` and `http/dup`, `database` opt-in value, the HTTP and network attribute renames in the table, schema URL form, schema translate processor mention, opt-in variable scope.
- Removed (unconfirmed): "HTTP (2023) / DB (2025)" stable dates, messaging and gen_ai stability statements, `messaging/dup`, Java agent 2.x semconv default, Prometheus suffix names, the claim that the collector schema processor is "in development".
Method: documentation only; no commands were run.
