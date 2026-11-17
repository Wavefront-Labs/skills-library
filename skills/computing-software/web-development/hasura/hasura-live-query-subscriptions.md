---
id: computing-software.web-development.hasura.hasura-live-query-subscriptions
name: hasura-live-query-subscriptions
category: computing-software
field: web-development
product: hasura
tags: [hasura, subscriptions, live-query, multiplexing, websocket]
level: practitioner
status: docs-checked
description: "Turn a Hasura query into a live subscription over /v1/graphql and understand how multiplexing batches similar subscriptions into one SQL query."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/subscriptions/postgres/livequery/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/subscriptions/postgres/livequery/execution.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: push fresh query results to clients as data changes.

Steps:
1. Change the operation keyword from `query` to `subscription`:

```graphql
subscription {
  author(where: { id: { _eq: 1 } }) { id name }
}
```
2. Subscriptions are live queries executed over the WebSocket protocol.
3. A live query returns the latest result, not each event leading to it. Updates are delivered every 1 second by default; the first result is emitted at start, and later results only when the query result changes.

Multiplexing, per the docs: similar subscriptions are batched into a single SQL query. Batching requires the same role, the same selection set (arguments differing only in scalar values), and the same connection template if dynamic routing is used. Batch size is set with `HASURA_GRAPHQL_LIVE_QUERIES_MULTIPLEXED_BATCH_SIZE` (default 100, flag `--live-queries-multiplexed-batch-size`).

Multiplexing details: the operation name does not prevent it, but an alias on a field does (so `name: user_name` versus `name` will not batch together). Hasura diff-checks the batched responses and sends a result only to clients whose data changed.

Constraints: a subscription may only have one root field, and you cannot run several subscriptions in one operation; use separate requests.

Gotcha: subscriptions that rely on SQL functions (custom root fields or computed fields) may hit multiplexing errors if the function throws "dynamic" exceptions based on table data (for example by checking an aggregate); exceptions based on static input arguments are safe. Setting `HASURA_GRAPHQL_LIVE_QUERIES_MULTIPLEXED_BATCH_SIZE` to 1 avoids the problem.

## Checked

2026-11-04. Confirmed against the cited pages: livequery index and execution pages: query-to-subscription conversion, 1 s default, WebSocket execution, multiplexing criteria, batch size flag and default, alias behaviour, single root field, SQL function limitation and batch-size-1 workaround. Removed or corrected: the claim that both subscriptions-transport-ws and graphql-ws are supported and that `/v1/graphql` is the endpoint (not on the cited pages), and the Verify step.

Method: documentation only; no commands were run.
