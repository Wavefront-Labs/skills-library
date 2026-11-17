---
id: computing-software.database-administration.dragonfly.migrate-replication-from-redis
name: migrate-replication-from-redis
category: computing-software
field: database-administration
product: dragonfly
tags: [migration, redis-migration, replicaof, cutover, dragonfly]
level: practitioner
status: docs-checked
description: "Migrate from Redis to Dragonfly with little downtime by replicating from the Redis primary, then promoting Dragonfly and repointing clients."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication-based migration:

Dragonfly supports Redis-Dragonfly replication for migrating Redis workloads. It supports the data structures and replication protocol of Redis OSS up to version 6.2, and the replica setup is the same as for Dragonfly-to-Dragonfly replication, with the primary being a running Redis server.

1. Run Dragonfly alongside the Redis primary.
2. On Dragonfly, run `REPLICAOF <redis-host> <redis-port>`. If Redis needs a password, start Dragonfly with the `masterauth` flag.
3. Check `INFO REPLICATION` on Dragonfly until the sync completes.
4. Cut over: run `REPLICAOF NO ONE` on Dragonfly, which stops replication and keeps the replicated dataset.
5. Repoint applications to Dragonfly.

Alternative with a downtime window: snapshot and restore (see migrate-snapshot-restore).

## Checked

2026-11-04. Confirmed in the Replication page (Redis-Dragonfly section, REPLICAOF NO ONE), the REPLICAOF page (`masterauth`) and the INFO page. The original source URL returned 404 and was replaced by the Replication page. Removed the Sentinel failover steps and the generic backup and rollback advice, which no fetched page states.

Method: documentation only; no commands were run.
