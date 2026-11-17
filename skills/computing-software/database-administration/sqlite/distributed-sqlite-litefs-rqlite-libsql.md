---
id: computing-software.database-administration.sqlite.distributed-sqlite-litefs-rqlite-libsql
name: distributed-sqlite-litefs-rqlite-libsql
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, litefs, rqlite, libsql, litestream, distributed-sqlite]
level: practitioner
status: verified
description: "Compare ways to replicate or distribute SQLite (LiteFS, rqlite, libSQL/Turso, Litestream, dqlite) by consistency, write path, failover and operational cost."
sources:
  - https://fly.io/docs/litefs/
  - https://fly.io/docs/litefs/how-it-works/
  - https://github.com/rqlite/rqlite.io/blob/master/content/en/docs/API/Read%20Consistency/_index.md
  - https://github.com/canonical/dqlite
  - https://rqlite.io/docs/
  - https://docs.turso.tech/libsql
  - https://litestream.io/how-it-works/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed SQLite (LiteFS / rqlite / libSQL)

SQLite is single-node by design. These tools add replication; they differ in where writes go and what consistency you get.

| Tool | Mechanism | Writes | Reads | Failover |
|---|---|---|---|---|
| Litestream | Streams WAL changes (LTX files in v0.5) to S3-compatible/object storage; optional VFS read replicas | Single node | Single node (restore elsewhere) | Manual restore; DR not HA |
| LiteFS | FUSE filesystem captures transactions, ships LTX files to replicas | Primary only (lease via Consul or static) | Local on every replica (async, eventually consistent) | Lease handover; replicas lag |
| rqlite | Raft consensus; SQLite per node; HTTP API | Leader, committed by quorum | Levels: none / weak (default) / linearizable / strong | Automatic leader election |
| dqlite | Raft-based replication in an embeddable C library (canonical/dqlite README) | Leader | Leader | Automatic |
| libSQL / Turso | Fork of SQLite (same file format); embedded replicas | Remote primary by default (`offline` option allows local writes) | Local replica file, synced on demand or every `syncInterval` seconds | Managed by service |

## Choosing
- Backup/DR for a single app server → Litestream (cheap, simple).
- Read-heavy app on edge nodes with one write region → LiteFS or libSQL embedded replicas; route writes to the primary (LiteFS proxy forwards POST/PUT writes with the `fly-replay` header and makes GETs wait for the replication position). Fly.io's LiteFS page says it cannot provide support for the product and warns against combining it with Machine autostop/autostart (a stale node can win the lease and newer changes be discarded), so check its current status before adopting. For new Turso projects the docs recommend Turso Sync over embedded replicas.
- Need strongly consistent writes and automatic failover → rqlite/dqlite; accept higher write latency (quorum round trips) and an API instead of direct file access.

## Gotchas
- rqlite replicates statements, so non-deterministic SQL can diverge nodes. It rewrites `RANDOM()`/`RANDOMBLOB(N)` and date/time functions before writing to the Raft log, but not `RANDOM()` inside `ORDER BY` (e.g. `INSERT ... SELECT ... ORDER BY RANDOM()`); see the rqlite non-deterministic functions page.
- Async replicas can serve stale reads right after a write; use read-your-writes routing (TXID tracking in the LiteFS proxy; libSQL embedded replicas read your own writes by default). rqlite levels are weak (default), linearizable, strong, none (plus auto); `none` reads can be stale on followers.
- LiteFS is a FUSE filesystem: the app must open the database through the mount. It captures changes from both rollback-journal (DELETE/PERSIST/TRUNCATE) and WAL modes (how-it-works page). The default cluster lease uses Consul; a `static` lease assigns one fixed primary with no failover.

## Verify
Kill the primary/leader in staging: measure write unavailability and confirm no committed write is lost (for consensus tools) or measure the data-loss window (for async tools).
