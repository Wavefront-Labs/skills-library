---
id: computing-software.web-development.hasura.hasura-async-actions
name: hasura-async-actions
category: computing-software
field: web-development
product: hasura
tags: [hasura, actions, async, subscriptions, action-log]
level: advanced
status: docs-checked
description: "Run long Hasura Action mutations asynchronously, receive an action_id and subscribe to the result, and clean up hdb_action_log safely."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/async-actions.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/logs-clean-up.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle slow operations without holding the request open.

Only actions of type `mutation` can be async; queries are always synchronous. Mark the action asynchronous when creating it. Calling it returns an `action_id` (a uuid) immediately, before the handler is contacted:

```graphql
mutation placeOrderRequest($order_input: place_order_input!) {
  place_order(input: $order_input)
}
```
For each async action Hasura also generates a query and a subscription field named after the action, taking the action id:

```graphql
subscription getPlaceOrderResponse {
  place_order(id: "<ACTION_ID>") {
    output
    errors
  }
}
```
Logs live in `hdb_catalog.hdb_action_log` in the metadata database.

Log cleanup: the docs prune with SQL, for example:

```sql
DELETE FROM hdb_catalog.hdb_action_log WHERE created_at < NOW() - INTERVAL '3 months';
```
Other documented forms filter by `id` or `action_name`. The docs say these steps are for self-hosted Enterprise Edition; Cloud customers should ask support.

Gotcha: deleting is irreversible, and deleting logs while subscriptions for the response may be open can lose data and return `null`. Also, for async actions you cannot have nested object types and relationships in the same action.

## Checked

2026-11-04. Confirmed against the cited pages: async-actions, logs-clean-up and custom types pages: mutation-only rule, action_id, generated query/subscription fields, log table, DELETE examples, irreversibility and null warning, EE/Cloud note, nested-objects-with-relationships limit. Removed or corrected: Console field labels and `kind: asynchronous` (not on the cited pages), the invented subscription variable form, scheduled-trigger suggestion and the Verify step.

Method: documentation only; no commands were run.
