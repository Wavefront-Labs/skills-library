---
id: computing-software.cloud-infrastructure-engineering.observability.otel-database-and-messaging-semantic-conventions
name: otel-database-and-messaging-semantic-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [db-semantic-conventions, messaging-semantic-conventions, semantic-conventions, span-naming, span-links]
level: advanced
status: docs-checked
description: "Apply OTel database and messaging semantic conventions: db.* attributes, query sanitisation, span naming, producer/consumer span kinds, batch links and duration metrics."
sources: ["https://opentelemetry.io/docs/specs/semconv/database/database-spans/", "https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/", "https://opentelemetry.io/docs/specs/semconv/database/database-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database and messaging semantic conventions

## Database client spans (page status: Stable, unless otherwise specified)
- Span kind CLIENT. Name: `{db.query.summary}` if available, else `{db.operation.name} {target}` (e.g.
  `SELECT orders`), else `{db.system.name}`.
- Attributes: `db.system.name` (renamed from `db.system`: `postgresql`, `mysql`, `mongodb`, `redis`...),
  `db.namespace` (database/schema), `db.collection.name` (table), `db.operation.name`, `db.query.text`
  (**sanitised**: literals replaced by `?`), `db.query.summary`, `db.response.status_code`, `server.address`,
  `server.port`, `error.type`, `db.operation.batch.size`.
- Metric: `db.client.operation.duration` (seconds histogram); connection pool metrics `db.client.connection.count`
  and `db.client.connection.pending_requests` (see the database metrics page for the rest).
- Migration from old names (`db.statement`, `db.name`, `db.sql.table`) via `OTEL_SEMCONV_STABILITY_OPT_IN=database`
  (or `database/dup` to emit both during transition).

## Messaging spans (development status - expect changes)
- Span kinds: PRODUCER for create/send; the page also defines receive, process and settle spans, so read it for their kinds.
- Name: `{messaging.operation.name} {destination}` -> `send orders`, `process orders`.
- Attributes: `messaging.system` (`kafka`, `rabbitmq`, `aws_sqs`), `messaging.destination.name`,
  `messaging.operation.type` (`create|send|receive|process|settle`), `messaging.message.id`,
  `messaging.batch.message_count`, `messaging.destination.partition.id`. Kafka-specific attributes live on the separate Kafka conventions page.
- Context: producer injects trace context into message headers; the process span is a child of (or **linked** to)
  the producer span. For batch receive, create one span with **links** to each message's context - a span can have
  only one parent.
- Metrics: `messaging.client.sent.messages` and others on the messaging metrics page.

## Gotchas
- Unsanitised `db.query.text` leaks PII and explodes cardinality in span-metrics if used as a dimension.
- Do not use `db.query.text` as span name.
- Long-lived consumer loops must create a new span per message, not one span for the loop.

## Checked
Checked 2026-10-28 against semantic-conventions pages: database spans, database metrics, messaging spans (spec site, semconv 1.x as served on that date).
- Confirmed: CLIENT span kind for DB, `db.system.name`, `db.query.summary`, `db.query.text` (opt-in, sanitised with `?` placeholder), `db.operation.batch.size`, `db.response.status_code`, `db.client.operation.duration`, `db.client.connection.count`, `db.client.connection.pending_requests`, `OTEL_SEMCONV_STABILITY_OPT_IN` with `database/dup`, messaging span name `{messaging.operation.name} {destination}`, PRODUCER kind, `messaging.operation.type`, `messaging.message.id`, `messaging.batch.message_count`, `messaging.destination.partition.id`, `messaging.client.sent.messages`, single-parent limit motivating span links, messaging spans page status Development.
- Removed: "stable since 2025", `db.client.connection.wait_time`, `messaging.consumer.group.name`, `messaging.kafka.*` names, `messaging.client.operation.duration`/`consumed.messages`, the CONSUMER and settle span-kind claims (not on the fetched pages).

Method: documentation only; no commands were run.
