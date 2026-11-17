---
id: computing-software.database-administration.valkey.replication-psync-and-ids
name: replication-psync-and-ids
category: computing-software
field: database-administration
product: valkey
tags: [replication, replicaof, psync, replication-id, offset, backlog, wait, waitaof, replica-announce-ip]
level: practitioner
status: docs-checked
description: "Valkey primary-replica replication: async model, replicaof, replication ID and offset, PSYNC partial resync, failover secondary ID, WAIT, NAT announce settings."
sources:
  - https://valkey.io/topics/replication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication is asynchronous leader-follower: the primary streams every dataset change (client writes, expirations, evictions); replicas ack their processed offset periodically. A primary can have many replicas, replicas can chain (not in cluster mode), and replication is non-blocking on the primary. `WAIT` and `WAITAOF` request acknowledged copies but do not make Valkey strongly consistent; acknowledged writes can still be lost in failover.

Setup: `replicaof 192.168.1.1 6379` in config, or the `REPLICAOF` command. In cluster mode use `CLUSTER REPLICATE <node-id>` instead. Replicas are read-only by default (`replica-read-only`). With a password primary, set `primaryauth <password>` (also settable with `CONFIG SET`).

Identity: each primary has a replication ID (a history) and an offset counting stream bytes, even with no replicas. The pair identifies an exact dataset. A replica sends its ID and offset with `PSYNC`; if the backlog still covers the gap and the history is known, only the missing part is sent, otherwise a full resync happens. A promoted replica keeps its old ID as a secondary ID (with the offset at switch) and generates a new main ID, so other replicas partially resync after failover without conflicting with a partitioned old primary. Replicas shut down with `SHUTDOWN` store resync data in the RDB; AOF-restarted replicas cannot partially sync.

Replicas do not expire keys themselves; the primary sends `DEL`. Replicas ignore `maxmemory` unless `replica-ignore-maxmemory no`.

NAT or containers: `replica-announce-ip 5.5.5.5` and `replica-announce-port 1234` change what `INFO replication` and `ROLE` report; cluster uses `cluster-announce-*`.

## Checked
2026-11-03. Confirmed against the Valkey Replication page (valkey.io/topics/replication/): asynchronous model with periodic acks, WAIT/WAITAOF limits, cascading replicas not available in cluster mode, `replicaof` and `CLUSTER REPLICATE`, `replica-read-only`, `primaryauth`, replication ID plus offset, PSYNC and backlog, secondary ID after promotion, SHUTDOWN storing resync data in the RDB, AOF restarts unable to partial sync, `replica-ignore-maxmemory`, and the announce settings. Nothing removed.
Method: documentation only; no commands were run.
