---
id: computing-software.web-development.hasura.hasura-cron-and-one-off-triggers
name: hasura-cron-and-one-off-triggers
category: computing-software
field: web-development
product: hasura
tags: [hasura, scheduled-triggers, cron, one-off, webhooks, cleanup]
level: practitioner
status: docs-checked
description: "Schedule webhooks with Hasura cron triggers in cron_triggers.yaml or one-off scheduled events via create_scheduled_event, with retries and cleanup."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/scheduled-triggers/how-it-works.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/scheduled-triggers/create-cron-trigger.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/scheduled-triggers/create-one-off-scheduled-event.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/scheduled-triggers/clean-up.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run timed jobs against an HTTP endpoint.

Cron trigger in `cron_triggers.yaml`:

```yaml
- name: eod_reports
  webhook: https://<HANDLER_HOST>/eod
  schedule: 0 22 * * 1-5
  include_in_metadata: true
  payload:
    scope: all
  retry_conf:
    num_retries: 3
    timeout_seconds: 120
    tolerance_seconds: 21675
    retry_interval_seconds: 12
```
Cron events are created from the UTC schedule. `include_in_metadata: true` keeps the trigger in the Hasura metadata. Console: `Events > Cron Triggers > Create`.

One-off events cannot be set through the CLI because they are not tracked as part of Hasura metadata. Use the Metadata API:

```json
{
  "type": "create_scheduled_event",
  "args": {
    "webhook": "https://<HANDLER_HOST>/once",
    "schedule_at": "2026-12-01T09:00:00Z",
    "payload": { "k": "v" }
  }
}
```
Cleanup tables in the metadata database: `hdb_catalog.hdb_cron_events`, `hdb_catalog.hdb_cron_event_invocation_logs`, `hdb_catalog.hdb_scheduled_events`, `hdb_catalog.hdb_scheduled_event_invocation_logs`. To clear processed events, delete rows `WHERE status IN ('delivered', 'error', 'dead')`.

Gotcha: for each Hasura Cloud project the retention period for cron events and cron invocation logs is 1 month.

## Checked

2026-11-04. Confirmed against the cited pages: scheduled-triggers create-cron-trigger, create-one-off-scheduled-event and clean-up pages: cron_triggers.yaml fields, retry_conf values, UTC, create_scheduled_event, CLI limitation, four hdb_catalog tables, status filter, Cloud 1 month retention. Removed or corrected: the tolerance_seconds meaning, retry/2xx statements and the Verify step.

Method: documentation only; no commands were run.
