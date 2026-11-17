---
id: computing-software.cloud-infrastructure-engineering.observability.choosing-logs-and-events
name: choosing-logs-and-events
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [when-to-use-logs, log-events, telemetry-signals, signal-selection, high-cardinality]
level: practitioner
status: draft
description: "Decide when a question needs logs or discrete events rather than metrics: high-cardinality context, audit, debugging detail. Covers structure, volume and log-vs-metric tradeoffs."
sources: ["https://opentelemetry.io/docs/concepts/signals/logs/", "https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/", "https://sre.google/workbook/monitoring/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing logs or events

Logs are per-event records. They keep identity and arbitrary-cardinality context that metrics throw away, and
they cost per byte ingested and stored.

## Use logs/events when
- You need **who/what/which**: user ID, tenant, request ID, order ID, SQL statement, exception and stack.
- The event is **discrete and meaningful on its own**: deploy, config change, auth failure, job start/finish,
  state transition. Model those as structured events with a stable `event.name`.
- **Audit/compliance** requires the individual record (retained per policy, often separately).
- You are **debugging after the fact** and cannot predict the dimension you will slice on.

## Prefer a metric instead when
You only ever count them. `level=error` lines counted in LogQL every 30 s for an alert is a log query doing a
metric's job: instrument a counter (`errors_total{reason}`), keep the log for the detail.

## Events vs logs
An event is a log record with a name and schema (OTel: `event.name` attribute on a LogRecord). Treat events as an
API: document fields, version them, do not rename casually. Free-text logs are for humans; events are for queries.

## Making logs useful
- Structured (JSON or logfmt), one event per line, consistent field names (see log schema skill).
- Always include `trace_id`/`span_id` when in a request, `service.name`, `deployment.environment`.
- Message stays constant; variables go in fields (`"payment declined", reason=insufficient_funds`), so you can group.

## Volume control
Logs are the most expensive signal at scale. Log on state change and failure, not on every success in a hot
loop; sample debug/info for high-volume paths; drop health-check access logs at the agent.

## Loki-specific choice
In Loki, high-cardinality values belong in the log line or structured metadata, never in stream labels.
