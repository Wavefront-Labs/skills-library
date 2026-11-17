---
id: computing-software.data-engineering.snowflake.append-only-streams-and-streams-on-views
name: append-only-streams-and-streams-on-views
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, append-only-stream, insert-only-stream, streams-on-views, change-tracking]
level: advanced
status: docs-checked
description: "Choose Snowflake stream types: standard vs append-only vs insert-only, streams on views and shared tables, change tracking prerequisites, and staleness."
sources:
  - https://docs.snowflake.com/en/user-guide/streams-intro
  - https://docs.snowflake.com/en/sql-reference/sql/create-stream
  - https://docs.snowflake.com/en/user-guide/streams-manage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Append-only / insert-only streams and streams on views

**Goal:** consume only the changes you need, cheaply, from tables, views and external sources.

## Types
```sql
CREATE STREAM orders_std ON TABLE raw.orders;                     -- inserts, updates, deletes (net)
CREATE STREAM events_ins ON TABLE raw.events APPEND_ONLY = TRUE;  -- inserts only
CREATE STREAM ext_files ON EXTERNAL TABLE raw.ext_logs INSERT_ONLY = TRUE;  -- external table
```
- **Standard**: net delta (row inserted then deleted between offsets = nothing).
- **Append-only** (`APPEND_ONLY = TRUE`): tracks inserts only.
- **Insert-only** (`INSERT_ONLY = TRUE`): used for streams on external tables (see CREATE STREAM).

## Streams on views
```sql
ALTER TABLE raw.orders SET CHANGE_TRACKING = TRUE;      -- every base table
ALTER TABLE raw.customers SET CHANGE_TRACKING = TRUE;
CREATE STREAM orders_v_stream ON VIEW analytics.orders_enriched;
```
- Views with GROUP BY, QUALIFY, LIMIT or DISTINCT clauses, correlated subqueries, or subqueries outside the FROM clause are not supported (streams docs, streams on views).

## Initial rows and staleness
- `SHOW_INITIAL_ROWS = TRUE` returns current rows on first read (bootstrap).
- A stream goes **stale** if not consumed within the table's data retention, extended up to `MAX_DATA_EXTENSION_TIME_IN_DAYS` (default 14). Check `SHOW STREAMS` -> `stale_after`.
- The offset advances when a DML statement consumes the stream.

## Gotchas
- Truncate/reload pattern on the source with a standard stream produces deletes + inserts of everything; use append-only.
- Multiple consumers need one stream each.

## Verify
`SELECT SYSTEM$STREAM_HAS_DATA('events_ins')` returns true after an insert.

## Checked
2026-10-28. Confirmed against the Snowflake CREATE STREAM and streams introduction pages (APPEND_ONLY and INSERT_ONLY options, SHOW_INITIAL_ROWS, CHANGE_TRACKING, standard streams record net changes including truncates, unsupported view constructs, staleness extended up to 14 days by default, stale_after, SYSTEM$STREAM_HAS_DATA, one stream per consumer). Removed: cost remarks, external-table-only and Iceberg claims, union and secure view claims, the shared-table remark, commit-time offset wording, the CREATE OR REPLACE claim and the update-leaves-empty verification.
Method: documentation only; no commands were run.
