---
id: computing-software.web-development.hasura.hasura-streaming-subscriptions
name: hasura-streaming-subscriptions
category: computing-software
field: web-development
product: hasura
tags: [hasura, subscriptions, streaming, cursor, websocket]
level: advanced
status: docs-checked
description: "Stream rows from Hasura with cursor-based streaming subscriptions, tune batch size and refetch interval, and handle non-unique cursor columns."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/subscriptions/postgres/streaming/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/subscriptions/postgres/streaming/use-cases.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: receive new rows incrementally rather than only the latest value of the result set.

Availability: Hasura GraphQL Engine v2.7.0-beta.1 and above. The server keeps a cursor value per subscription and updates it after each batch, so Hasura does not require sticky sessions.

Each stream field takes a cursor with an initial value and ordering, and a batch size (example from the docs):

```graphql
subscription getUndeliveredMessages {
  messages_stream(cursor: { initial_value: { created_at: "2022-01-01" }, ordering: ASC }, batch_size: 2) {
    id
    content
    created_at
  }
}
```
Each response then continues after the greatest cursor value sent in the previous one.

Server tuning env vars (multiplexed batch size and refetch interval):
- `HASURA_GRAPHQL_STREAMING_QUERIES_MULTIPLEXED_BATCH_SIZE`
- `HASURA_GRAPHQL_STREAMING_QUERIES_MULTIPLEXED_REFETCH_INTERVAL`

Notes from the docs:
- Choose a cursor that is unique and sortable so each row is sent exactly once.
- A cursor on a non-unique column: on Postgres and Citus the data is correct but some responses can be larger than the batch size (`FETCH FIRST n WITH TIES` is used). On Postgres-like databases without WITH TIES, such as Cockroach, rows may be skipped when the column has duplicates.
- Use cases listed: undelivered messages in a chat application, subscribing only to changed events, and processing out-of-order events (such as cart updates) in creation order.

Gotcha: do not use time-dependent Postgres special values such as `now`, `today`, `tomorrow` or `yesterday` as the cursor `initial_value`. The value is sent as text and converted on every poll, so `now` means the latest poll, and rows inserted between polls can be missed. Pass a concrete timestamp computed by the client, for example "2022-06-15T10:00:00Z".

## Checked
2026-11-07. Read in full both cited pages (index.mdx and use-cases.mdx; GitHub file view, no snippet files).
Confirmed: version, sticky-session note, env var names, non-unique cursor behaviour, Cockroach warning, use cases, the special-value warning, the stream example.
Removed: the claim that special values are "re-evaluated on every poll" as a feature (the page warns against using them), the `select_stream` permission gotcha (not on the pages), the `message_stream` example (page uses `messages_stream`), and the invented Verify step.
Method: documentation only; no commands were run.
