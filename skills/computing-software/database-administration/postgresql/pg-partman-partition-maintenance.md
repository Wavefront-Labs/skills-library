---
id: computing-software.database-administration.postgresql.pg-partman-partition-maintenance
name: pg-partman-partition-maintenance
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-extensions, create-extension, pg-partman, table-partitioning, partition-retention, run-maintenance, time-partitioning, premake]
level: advanced
status: docs-checked
description: "Automate PostgreSQL time/id partition creation and retention with pg_partman 5: create_parent, premake, retention, run_maintenance scheduling and the default partition."
sources:
  - https://github.com/pgpartman/pg_partman/blob/master/doc/pg_partman.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_partman

**Goal:** future partitions always exist before rows arrive, old ones are
dropped or detached on schedule, nobody runs DDL by hand.

## Setup (native partitioning)
```sql
CREATE SCHEMA partman;
CREATE EXTENSION pg_partman SCHEMA partman;

CREATE TABLE public.events (id bigint GENERATED ALWAYS AS IDENTITY, created_at timestamptz NOT NULL, payload jsonb)
  PARTITION BY RANGE (created_at);

SELECT partman.create_parent(
  p_parent_table   => 'public.events',
  p_control        => 'created_at',
  p_interval       => '1 day',
  p_premake        => 7);          -- keep 7 future partitions ready
```
A `events_default` partition is created to catch rows outside existing ranges.

## Retention
```sql
UPDATE partman.part_config
SET retention = '90 days', retention_keep_table = false,   -- true = detach only
    infinite_time_partitions = true                       -- keep premaking even with no new data
WHERE parent_table = 'public.events';
```

## Run maintenance on a schedule
Either the background worker:
```conf
shared_preload_libraries = 'pg_partman_bgw'
pg_partman_bgw.interval = 3600
pg_partman_bgw.dbname = 'appdb'
```
or pg_cron: `SELECT cron.schedule('partman', '7 * * * *', $$CALL partman.run_maintenance_proc()$$);`

## Gotchas
- Rows landing in the default partition mean the premade partitions did not cover them.
  Monitor with `partman.check_default()` and move rows with
  `partman.partition_data_proc('public.events')`, which commits in smaller batches.

## Verify
```sql
SELECT partman.show_partitions('public.events');   -- future partitions present
SELECT * FROM partman.check_default();             -- default partitions with rows
```

## Checked

2026-10-28. Confirmed against the pg_partman documentation (pg_partman.md on GitHub): create_parent with p_parent_table, p_control, p_interval, p_premake, an automatically created default partition, part_config retention, retention_keep_table (default true) and infinite_time_partitions (default false), run_maintenance_proc, pg_partman_bgw.interval and pg_partman_bgw.dbname, show_partitions, check_default, partition_data_proc. Removed unconfirmed: the 5.x/4.x upgrade note, the default-partition error text, primary key rule, ACCESS EXCLUSIVE note.

Method: documentation only; no commands were run.
