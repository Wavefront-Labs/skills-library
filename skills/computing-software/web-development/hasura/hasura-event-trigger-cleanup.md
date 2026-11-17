---
id: computing-software.web-development.hasura.hasura-event-trigger-cleanup
name: hasura-event-trigger-cleanup
category: computing-software
field: web-development
product: hasura
tags: [hasura, event-triggers, cleanup, event-log, maintenance]
level: practitioner
status: docs-checked
description: "Keep Hasura event log tables small by cleaning hdb_catalog.event_log and event_invocation_logs manually or with automatic cleanup on Cloud and Enterprise."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/clean-up/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/event-triggers/clean-up/auto-cleanup.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop event history from growing forever.

Event data lives in the `hdb_catalog` schema of the database that holds the source table. Tables: `hdb_catalog.event_log` (all captured events) and `hdb_catalog.event_invocation_logs` (HTTP requests and responses). The docs give plain SQL cleanup options:
- clear only HTTP logs: `DELETE FROM hdb_catalog.event_invocation_logs;`
- clear only processed events: `DELETE FROM hdb_catalog.event_log WHERE delivered = true OR error = true;`
- one trigger only: filter by `trigger_name = '<event_trigger_name>'`
- by age: add `created_at < now() - interval '3 months'` to the where clause
- everything, including events not yet delivered (Option 5), or `TRUNCATE hdb_catalog.event_invocation_logs, hdb_catalog.event_log;` on large tables (it takes an exclusive lock and cannot take a WHERE).

Auto cleanup (from v2.13; Cloud and Enterprise editions) is configured per trigger in the `cleanup_config`, in the Console under the trigger's `Modify` tab, `Auto-cleanup Event Logs`, or in metadata:

```yaml
cleanup_config:
  clear_older_than: 168
  schedule: "0 0 * * *"
  clean_invocation_logs: true
  batch_size: 10000
  timeout: 60
  paused: false
```
Fields: `clear_older_than` minimum age in hours; `schedule` a cron expression (the example `0 0 * * *` is daily at 00:00 UTC); `clean_invocation_logs` (default false); `batch_size` (default 10000); `timeout` seconds per batch (default 60; a batch that times out halts the rest of that run); `paused` (default false).

Manage cleaners with the Metadata APIs `cleanup_event_trigger_logs` (manual), `pause_event_trigger_cleanups` and `resume_event_trigger_cleanups`.

Gotcha: if you first choose not to delete invocation logs and later want them gone, you must delete the retained logs manually.

## Checked

2026-11-04. Confirmed against the cited pages: clean-up index and auto-cleanup pages: tables, SQL options, TRUNCATE caveat, v2.13, cleanup_config parameters and defaults, Console location, management APIs, retained-logs warning. Removed or corrected: the `run_sql` claim, the export-first/slow-processing gotcha and the Verify step.

Method: documentation only; no commands were run.
