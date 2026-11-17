---
id: computing-software.web-development.hasura.hasura-event-trigger-payload-and-tuning
name: hasura-event-trigger-payload-and-tuning
category: computing-software
field: web-development
product: hasura
tags: [hasura, event-triggers, payload, performance, env-vars]
level: advanced
status: docs-checked
description: "Read the Hasura event trigger webhook payload and tune event delivery throughput with fetch batch size, HTTP pool size and fetch interval."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/payload.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/observability-and-performance.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/serverless.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: parse events correctly and scale delivery.

Payload shape:

```json
{
  "event": {
    "op": "INSERT",
    "data": { "old": null, "new": { "id": 1 } },
    "session_variables": { "x-hasura-role": "user" },
    "trace_context": { "span_id": "<SPAN_ID>", "trace_id": "<TRACE_ID>" }
  },
  "created_at": "<TIMESTAMP>",
  "id": "<UUID_FOR_INVOCATION>",
  "delivery_info": { "current_retry": 0, "max_retries": 3 },
  "trigger": { "name": "notify_new_user" },
  "table": { "schema": "public", "name": "users" }
}
```
`op` is INSERT, UPDATE, DELETE or MANUAL. Delivery is an HTTP `POST` with `Content-Type: application/json`; the docs print the object under a `payload` key and read it in a handler as `req.body.event.data.new.id`. `old` is null on INSERT and MANUAL, `new` is null on DELETE. `session_variables` is Postgres only. On Postgres UPDATE events are delivered only when new data differs from old, and table computed fields are not in the payload data.

Response: a `2xx` status counts as success; any other status is a failure retried per the retry config. A `Retry-After` header (seconds) on a non-2xx response makes Hasura redeliver once more after that time.

How it works: database triggers write per-row changes to Hasura's event tables (a queue). A poller thread fetches pending events in batches into an in-memory queue, and polling pauses while all HTTP workers are busy; a pool of HTTP workers delivers them to the webhook. Tuning env vars:
- `HASURA_GRAPHQL_EVENTS_FETCH_BATCH_SIZE` (default 100): larger batches lower database load and raise throughput but lengthen each fetch and may use more memory
- `HASURA_GRAPHQL_EVENTS_HTTP_POOL_SIZE` (default 100): more concurrent deliveries, at the cost of memory and CPU
- `HASURA_GRAPHQL_EVENTS_FETCH_INTERVAL` (default 1000 ms): a longer interval lowers database load but adds event latency

Diagnosis (Prometheus metrics are Enterprise Edition): high `hasura_event_fetch_time_per_batch_seconds` points at a slow database; high `hasura_event_queue_time_seconds` or active workers near the pool size (`hasura_event_trigger_http_workers`) means worker saturation, so raise the pool size; high `hasura_event_webhook_processing_time_seconds` means a slow webhook. If `hasura_events_fetched_per_batch` stays near the batch size, events may be waiting in the database.

The serverless page shows pointing triggers at serverless functions such as AWS Lambda, with examples in the community boilerplates.

## Checked

2026-11-04. Confirmed against the cited pages: payload, observability-and-performance and serverless pages: payload keys, ops, delivery and Retry-After, poller and worker description, three env vars with defaults and effects, EE metrics and golden-signal guidance. Removed or corrected: the raising-batch-size-queues-in-memory gotcha (the page says polling pauses when workers are busy) and the Verify step.

Method: documentation only; no commands were run.
