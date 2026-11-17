---
id: computing-software.database-administration.mysql.pt-online-schema-change
name: pt-online-schema-change
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, online-schema-change, pt-online-schema-change, percona-toolkit, trigger-based-migration, alter-foreign-keys-method, max-load, chunk-time]
level: advanced
status: docs-checked
description: "Alter large MySQL/MariaDB tables online with pt-online-schema-change: trigger-based copy, foreign key handling, load and lag throttling, and safe dry runs."
sources:
  - https://docs.percona.com/percona-toolkit/pt-online-schema-change.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pt-online-schema-change

**Goal:** an online ALTER that also works where gh-ost cannot (foreign keys,
Galera/PXC, statement binlogs), with controlled load.

## How it works
Creates `_orders_new` with the new definition, adds AFTER INSERT/UPDATE/DELETE
triggers on the original to mirror changes, copies rows in chunks sized to
`--chunk-time` (0.5 s default), then atomically renames.

## Run
```bash
pt-online-schema-change \
  --alter "ADD COLUMN note VARCHAR(255) NULL, ADD INDEX idx_note (note)" \
  D=appdb,t=orders,h=primary,u=admin --ask-pass \
  --max-load Threads_running=50 --critical-load Threads_running=200 \
  --max-lag 2 --check-replication-filters \
  --recursion-method=dsn=D=percona,t=dsns \
  --alter-foreign-keys-method=auto \
  --dry-run          # then repeat with --execute
```
`--recursion-method` tells it how to find replicas to watch for lag
(processlist default may miss replicas behind proxies).

## Foreign keys
Child tables reference the old table; after the swap they would point to the
renamed old copy. `--alter-foreign-keys-method`:
- `rebuild_constraints`: ALTER child tables to point to the new table (blocking
  ALTER on children; fine if they are small).
- `drop_swap`: disable FK checks, drop the old table, rename new: brief window
  where the table does not exist; no rollback.
- `auto`: picks rebuild_constraints when children are small enough.

## Gotchas
- Triggers add write overhead to every DML on the table during the copy
  (roughly doubling write cost); throttle aggressively on busy primaries.
- Existing triggers on the table: supported only with `--preserve-triggers` (MySQL 5.7.2+).
- Needs a PK or unique index for chunking.
- Creating triggers takes a metadata lock: a long transaction on the table blocks
  it; tool retries (`--tries create_triggers:...`), set `--set-vars lock_wait_timeout=5`.
- An aborted run leaves triggers and `_new` table; rerun cleans up or drop manually.

## Verify
Tool output ends with `Successfully altered`; `SHOW TRIGGERS LIKE 'orders'` is
empty; row counts match (`pt-table-checksum` on replicas if paranoid).

## Checked

2026-10-31: confirmed against the Percona Toolkit pt-online-schema-change reference page (fetched this batch): trigger-based copy with `--new-table-name` default `%T_new` (the tool prefixes underscores, so `_orders_new`), `--chunk-time` default 0.5, `--[no]check-replication-filters`, foreign-key methods (`rebuild_constraints`, `drop_swap`, `auto`), `--preserve-triggers`, `--max-load`/`--critical-load`, `--max-lag`, `--recursion-method` (incl. `dsn=`), `--dry-run`/`--execute`, `--set-vars`, `--history-table`. No claims removed.
Method: documentation only; no commands were run.
