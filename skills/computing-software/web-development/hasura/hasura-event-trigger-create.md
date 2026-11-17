---
id: computing-software.web-development.hasura.hasura-event-trigger-create
name: hasura-event-trigger-create
category: computing-software
field: web-development
product: hasura
tags: [hasura, event-triggers, webhooks, postgres, retry]
level: practitioner
status: docs-checked
description: "Create Hasura event triggers on Postgres or MS SQL tables to call a webhook on insert, update, delete or manual invocation, with retry settings."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/create-trigger.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/invoke-trigger-manually.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/remove-event-triggers.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: react to data changes with an HTTP call. Supported for Postgres and MS SQL Server. Console: `Events` tab, `Create`.

Metadata, in the table yaml under `event_triggers:`:

```yaml
event_triggers:
  - name: notify_new_user
    definition:
      enable_manual: true
      insert:
        columns: "*"
      update:
        columns: [email]
    webhook: https://<HANDLER_HOST>/hook
    retry_conf:
      num_retries: 3
      interval_sec: 10
      timeout_sec: 60
    headers:
      - name: X-Api-Key
        value_from_env: HOOK_KEY
```
Defaults for `retry_conf`: `num_retries` 0, `interval_sec` 10, `timeout_sec` 60.

APIs: `pg_create_event_trigger` (`mssql_create_event_trigger`), `pg_delete_event_trigger` (`mssql_delete_event_trigger`) and `pg_invoke_event_trigger` (manual invoke; needs `enable_manual` true at creation). Console: `Data -> [table-name] -> Browse Rows`, the `invoke trigger` button next to a row. Delete: `Delete Event Trigger` button on the trigger page.

The webhook URL must be a `POST` handler and can come from an environment variable. Headers take either a static `value` or `value_from_env`. `update.columns` lists the columns that trigger the webhook on update. On MS SQL Server, UPDATE triggers only work on tables with a primary key.

Guarantees: delivery is at least once and may be out of order, so handlers must be idempotent.

Gotcha: different Hasura instances acting on the same database can cause undefined behaviour at run time unless they share the same metadata.

## Checked

2026-11-04. Confirmed against the cited pages: create-trigger, invoke-trigger-manually and remove-event-triggers pages: supported databases, metadata YAML, retry defaults, headers, at-least-once delivery, API names, Console paths, MSSQL primary-key note, multi-instance caveat. Removed or corrected: the loses-delivery-after-one-failure claim (pages state only the retry default) and the Verify step.

Method: documentation only; no commands were run.
