---
id: computing-software.database-administration.mysql.gh-ost-online-migrations
name: gh-ost-online-migrations
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, online-schema-change, gh-ost, triggerless-migration, binlog-streaming, cut-over, throttling, postpone-cut-over]
level: advanced
status: docs-checked
description: "Alter large MySQL tables online with gh-ost: binlog-based copy, throttling on replica lag, controlled postponed cut-over, and the prerequisites that make it fail."
sources:
  - https://github.com/github/gh-ost/blob/master/doc/command-line-flags.md
  - https://github.com/github/gh-ost/blob/master/doc/requirements-and-limitations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gh-ost

**Goal:** change a hot multi-hundred-GB table with no blocking and replica lag
kept under control, cutting over at a moment you choose.

## How it works
Creates a ghost table `_orders_gho` with the new schema, copies rows in chunks,
and applies ongoing changes by **reading the binlog** (no triggers), then swaps
tables with an atomic RENAME at cut-over.

## Prerequisites
- `binlog_format=ROW`, `binlog_row_image=FULL` on the server gh-ost reads from
  (usually a replica: `log_replica_updates=ON`).
- Table must have a PRIMARY KEY or non-null unique key. No foreign keys
  (to or from) and no triggers on the table.
- User with ALTER, CREATE, DELETE, DROP, INDEX, INSERT, LOCK TABLES, SELECT, TRIGGER, UPDATE on the schema, plus SUPER and REPLICATION SLAVE (or REPLICATION CLIENT and REPLICATION SLAVE) on `*.*`.

## Typical run
```bash
gh-ost \
  --host=replica1 --database=appdb --table=orders \
  --alter="ADD COLUMN note VARCHAR(255), ADD INDEX idx_note (note)" \
  --chunk-size=1000 --max-load=Threads_running=50 --critical-load=Threads_running=200 \
  --max-lag-millis=1500 --throttle-control-replicas=replica2,replica3 \
  --postpone-cut-over-flag-file=/tmp/ghost.postpone \
  --serve-socket-file=/tmp/gh-ost.orders.sock \
  --initially-drop-ghost-table --ok-to-drop-table \
  --verbose --execute          # omit --execute for a dry run (--test-on-replica also exists)
```

## Control it live
```bash
echo throttle      | nc -U /tmp/gh-ost.orders.sock
echo no-throttle   | nc -U /tmp/gh-ost.orders.sock
echo "chunk-size=500" | nc -U /tmp/gh-ost.orders.sock
echo status        | nc -U /tmp/gh-ost.orders.sock
rm /tmp/ghost.postpone      # allow cut-over now
```

## Gotchas
- Cut-over takes a short lock on the original table; long-running queries on it
  delay cut-over (it retries with `--cut-over-lock-timeout-seconds`).
- Disk: needs space for a full copy of the table plus binlogs generated meanwhile.
- With `--host` a replica, gh-ost detects the source and writes there; check with `--assume-master-host` in complex topologies.
- Not usable with Galera/PXC or Group Replication multi-primary.
- Leftover `_gho`/`_ghc`/`_del` tables after aborts: drop them.

## Verify
`status` shows rows copied = estimated and `ETA: due`; after cut-over
`SHOW CREATE TABLE orders` has the change and `_orders_del` holds the old table
until you drop it.

## Checked

2026-10-31: confirmed requirements (MySQL 5.7+, row-based binlogs with FULL row image, primary key or non-null unique key, no foreign keys or triggers) and the documented privilege set on the gh-ost requirements-and-limitations doc; flags --cut-over-lock-timeout-seconds, --ok-to-drop-table, --postpone-cut-over-flag-file, --initially-drop-ghost-table, --assume-master-host, --test-on-replica, --serve-socket-file, --max-lag-millis, --critical-load on the command-line-flags doc; the `_gho`/`_ghc`/`_del` table naming in the gh-ost source (go/base/context.go, suffixes gho/ghc/ghk/del). Replaced the privilege summary with the documented list.
Method: documentation only; no commands were run.
