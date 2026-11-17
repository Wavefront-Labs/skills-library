---
id: computing-software.data-engineering.data-modelling.online-schema-change-mysql
name: online-schema-change-mysql
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-migration, gh-ost, pt-online-schema-change, mysql, online-ddl, instant-ddl, large-tables]
level: advanced
status: gated
description: "Alter large MySQL tables without downtime: native INSTANT/INPLACE DDL first, then gh-ost or pt-online-schema-change, with throttling, cut-over and CDC/replica impacts."
sources:
  - https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html
  - https://github.com/github/gh-ost/blob/master/doc/command-line-flags.md
  - https://docs.percona.com/percona-toolkit/pt-online-schema-change.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online schema change in MySQL

**Goal:** add columns/indexes or change types on a 500 GB production table with no blocking of writes and no replica lag storm.

## Step 1: can MySQL do it natively?
```sql
ALTER TABLE orders ADD COLUMN channel VARCHAR(20) NULL, ALGORITHM=INSTANT;          -- 8.0.12+ (any position 8.0.29+) (gated: unconfirmed, source is paywalled or blocked)
ALTER TABLE orders ADD INDEX idx_created (created_at), ALGORITHM=INPLACE, LOCK=NONE;
```
Specifying `ALGORITHM`/`LOCK` makes MySQL fail fast instead of silently copying the table. INSTANT: metadata-only (add/drop column, rename, default changes). INPLACE + LOCK=NONE: index builds, some changes, still heavy I/O and replicated as one long statement (replica lag equal to build time).

## Step 2: gh-ost (triggerless, binlog-based)
```bash
gh-ost \
  --host=replica-1 --database=shop --table=orders \
  --alter="MODIFY COLUMN amount DECIMAL(18,2) NOT NULL" \
  --assume-rbr \
  --chunk-size=1000 --max-load=Threads_running=50 --critical-load=Threads_running=200 \
  --max-lag-millis=1500 --throttle-control-replicas=replica-2,replica-3 \
  --postpone-cut-over-flag-file=/tmp/ghost.postpone \
  --exact-rowcount --concurrent-rowcount \
  --execute
```
How it works: creates a ghost copy of the table, copies rows in chunks, tails the binlog to apply ongoing changes, then swaps the tables at cut-over. `--assume-rbr` declares that the servers use row-based replication (`binlog_format=ROW`); it skips a STOP SLAVE/START SLAVE verification so gh-ost does not need the SUPER privilege. By default gh-ost connects to a replica and finds the master itself; `--allow-on-master` is needed to connect to the master directly. `--concurrent-rowcount` already defaults to true.
- Throttle on load and replica lag; interactive commands such as throttle are sent over the Unix socket set by `--serve-socket-file` (auto-determined if omitted).
- With `--postpone-cut-over-flag-file`, cut-over does not happen while the file exists; delete the file (or send the interactive cut-over command) to proceed.

## pt-online-schema-change (trigger-based)
```bash
pt-online-schema-change --alter "ADD INDEX idx_customer (customer_id)" \
  D=shop,t=orders --max-load Threads_running=50 --critical-load Threads_running=200 \
  --chunk-time 0.5 --max-lag 2 --execute
```
Uses triggers to capture changes: extra write load and issues with existing triggers/foreign keys (`--alter-foreign-keys-method`).

## Data pipeline impacts
- CDC tools that capture all tables will also see the tool's temporary tables: exclude them in the connector's table filters, and check the connector's logs after cut-over.
- Warehouse replication tools (Fivetran, DMS) may resync on table rename; check vendor guidance.

## Gotchas
- Foreign keys: gh-ost bails out when the migrated table has foreign keys (`--discard-foreign-keys` only drops them; `--skip-foreign-key-checks` only skips the check). pt-osc refuses unless you choose `--alter-foreign-keys-method`.
- Disk: needs space for a full table copy plus binlogs.
- Long-running transactions block the final rename (metadata lock); kill/avoid them at cut-over.

## Verify
- [ ] Dry run (`gh-ost` without `--execute`, `pt-osc --dry-run`) passes on the target.
- [ ] Replica lag stays below threshold during copy; CDC pipeline healthy after cut-over.

## Checked

- Date: 2026-11-02.
- Confirmed against: gh-ost command-line-flags page (--assume-rbr, --allow-on-master, --chunk-size, --max-load, --critical-load, --max-lag-millis, --throttle-control-replicas, --postpone-cut-over-flag-file, --serve-socket-file, --exact-rowcount, --concurrent-rowcount default, foreign-key behaviour); Percona pt-online-schema-change page (--max-load, --critical-load, --chunk-time, --max-lag, --dry-run/--execute, triggers, --alter-foreign-keys-method).
- Removed: the shadow-table suffix names, the Debezium rename claim and the socket one-liner (not stated in the fetched pages); the unneeded `--allow-on-master=false`.
- Gated: the MySQL ALGORITHM=INSTANT version gates (8.0.12, 8.0.29); the MySQL 8.0 online DDL page returned 403.

Method: documentation only; no commands were run.
