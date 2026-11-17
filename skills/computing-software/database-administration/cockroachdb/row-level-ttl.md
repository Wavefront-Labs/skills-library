---
id: computing-software.database-administration.cockroachdb.row-level-ttl
name: row-level-ttl
category: computing-software
field: database-administration
product: cockroachdb
tags: [row-level-ttl, ttl-expire-after, ttl-expiration-expression, ttl-job-cron, expired-data]
level: practitioner
status: docs-checked
description: "Expire rows automatically in CockroachDB with row-level TTL storage parameters: ttl_expiration_expression, ttl_expire_after, batching, rate limits, schedule and metrics."
sources:
  - https://www.cockroachlabs.com/docs/stable/row-level-ttl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: delete aged-out rows in the background without writing batch jobs.

Define expiry with a storage parameter (one or both):
```sql
CREATE TABLE ttl_test_per_row (id INT PRIMARY KEY, expired_at TIMESTAMPTZ)
  WITH (ttl_expiration_expression = 'expired_at', ttl_job_cron = '@daily');
CREATE TABLE ttl_test_per_table (id INT PRIMARY KEY)
  WITH (ttl_expire_after = '3 months', ttl_job_cron = '@daily');
```
`ttl_expiration_expression` is a SQL expression that must evaluate to `TIMESTAMPTZ`; `ttl_expire_after` is a fixed interval after create or update. `SHOW CREATE TABLE` then shows `ttl = 'on'`.

Tuning parameters: `ttl_select_batch_size`, `ttl_delete_batch_size`, `ttl_select_rate_limit`, `ttl_delete_rate_limit` (rate limits apply per node per table; they default to the matching `sql.ttl.*` cluster settings), `ttl_job_cron` (default `'@daily'`), `ttl_pause` to stop the job, `ttl_row_stats_poll_interval` to expose row counts as metrics, `ttl_disable_changefeed_replication` to keep TTL deletes out of changefeeds (cluster setting `sql.ttl.changefeed_replication.disabled`).

Behaviour: expired rows are eligible but not deleted immediately; a background job issues batched `SELECT` and `DELETE`. TTL reads use the elastic CPU limiter to reduce impact.

Metrics: `jobs.row_level_ttl.rows_selected`, `rows_deleted`, `select_duration`, `delete_duration`, `total_rows`, `total_expired_rows`. Per-table labels require `server.child_metrics.enabled = true` and the `ttl_label_metrics` storage parameter.

Verify: `SHOW CREATE TABLE` shows `ttl = 'on'` with your parameters, and `jobs.row_level_ttl.rows_deleted` increases after the job runs.

## Checked
2026-11-03. Confirmed on the row-level TTL page: both expiry parameters and example DDL, `SHOW CREATE TABLE` output with `ttl = 'on'`, tuning parameters and their `sql.ttl.default_*` cluster settings, per-node per-table rate limits, `@daily` default for `ttl_job_cron`, `ttl_pause`, `ttl_row_stats_poll_interval`, `ttl_disable_changefeed_replication` and `sql.ttl.changefeed_replication.disabled`, per-table metrics needing `server.child_metrics.enabled` and `ttl_label_metrics`. Removed: the (recommended) label, the rename gotcha, the admission control claim and the SHOW JOBS verify step.
Method: documentation only; no commands were run.
