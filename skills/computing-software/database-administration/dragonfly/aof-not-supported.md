---
id: computing-software.database-administration.dragonfly.aof-not-supported
name: aof-not-supported
category: computing-software
field: database-administration
product: dragonfly
tags: [aof, append-only-file, persistence, dragonfly]
level: intro
status: docs-checked
description: "Dragonfly does not support Append Only File persistence; use snapshots and replication for durability planning instead."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/aof.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AOF captures every write operation so it can be replayed at restart. **Dragonfly does not currently support AOF.**

The docs give the reason as lack of high-priority community demand, and note that implementing AOF would need a different and more sophisticated approach than Redis to keep performance high. The team says it is exploring the possibility for future releases and invites input on the Discord server.

Consequences for a Redis migration:

- Do not carry over `appendonly` expectations. Persistence options in Dragonfly are snapshots (automatic on shutdown, scheduled with `snapshot_cron`, manual with `SAVE` and `BGSAVE`) and replication.
- Snapshots capture state at a point in time, so writes after the last snapshot are lost if the instance dies without a replica.
- For higher safety, run one or more replicas and use `REPLICAOF`; on Kubernetes the Dragonfly Operator automates failover.

Check current status on the AOF page before relying on this, since the feature may be added.

## Checked

2026-11-04. Confirmed in the AOF page (not supported, reasons, exploring future support) and the Backups page (snapshot on shutdown when `dbfilename` is set, `snapshot_cron`, SAVE and BGSAVE via command pages). The data-loss bullet is a consequence of snapshot-only persistence. Nothing removed.

Method: documentation only; no commands were run.
