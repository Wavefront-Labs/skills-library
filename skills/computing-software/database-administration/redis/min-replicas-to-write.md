---
id: computing-software.database-administration.redis.min-replicas-to-write
name: min-replicas-to-write
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, replication, min-replicas-to-write, min-replicas-max-lag, wait, waitaof, sentinel, data-loss]
level: practitioner
status: docs-checked
description: "Bound data loss on a partitioned Redis primary with min-replicas-to-write / min-replicas-max-lag, and add WAIT or WAITAOF for per-write durability."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/replication/
  - https://redis.io/docs/latest/commands/wait/
  - https://redis.io/docs/latest/commands/waitaof/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
  - https://raw.githubusercontent.com/redis/redis/unstable/src/server.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# min-replicas-to-write

**Goal:** a primary isolated from its replicas stops accepting writes, bounding what is lost when Sentinel promotes a replica on the other side.

## Config
```text
min-replicas-to-write 1
min-replicas-max-lag 10
```
Defaults are `0` (feature off) and `10` seconds; setting either to 0 disables the feature. Both can be changed with
`CONFIG SET`. The primary refuses writes with `-NOREPLICAS Not enough good replicas to write.` unless at least N
replicas have a lag of at most M seconds. Replicas ping the primary every second, acknowledging how much of the replication stream they processed,
and the primary remembers the last ping time of each replica.

## Why
Replication is asynchronous: in a partition the old primary keeps accepting writes from clients on its side while Sentinel elects a new primary on the majority side. When it rejoins as a replica, those writes are discarded. With the settings above, the old primary stops after about 10 s, restricting the loss window to that time. The documentation calls it a best-effort data-safety mechanism: bounded loss is better than unbounded loss, but consistency is not ensured for a given write.

## Trade-off
Availability drops: if replicas are down or lagging, writes fail. With 1 replica and `min-replicas-to-write 1`, losing the replica stops writes. Use 2+ replicas with N=1.

## Per-write guarantees
```text
SET order:42 "..."
WAIT 1 100            # block until 1 replica acked or 100 ms; returns the number of replicas reached
WAITAOF 1 1 100       # 7.2+: write fsynced to local AOF and fsynced by 1 replica, or 100 ms; returns [local, replicas]
```
Neither `WAIT` nor `WAITAOF` makes Redis strongly consistent: a failover can still promote a replica without the write
(Sentinel and Cluster make a best effort to promote the best replica). They reduce the loss window for critical writes.
Both return counts on success and on timeout, so the client must check the counts. `WAITAOF` cannot run on a replica,
and `numlocal` must be 0 unless AOF is enabled locally. Clients decide what to do when fewer acks return.

## Cluster
Redis Cluster nodes that cannot reach the majority of masters for `cluster-node-timeout` stop accepting queries, which also
limits the minority-side write window.

## Verify
Block replication traffic (iptables) on a test primary: after `min-replicas-max-lag` seconds `SET` returns `NOREPLICAS`;
`INFO replication` shows `min_slaves_good_slaves:0`.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): replication page ("Allow writes only with
N attached replicas"), WAIT, WAITAOF, INFO, plus `redis.conf`, `src/config.c` and `src/server.c` from the redis/redis
repository. Confirmed: parameter names, defaults 0 and 10, CONFIG SET support, `NOREPLICAS` error text, replica
acknowledgement every second, WAIT and WAITAOF syntax and semantics (WAITAOF since 7.2.0), the consistency
caveats, `min_slaves_good_slaves`. Fixed: the replica-to-primary ping is not the `repl-ping-replica-period` setting
(that name was removed). Removed: "same settings apply per primary in Redis Cluster" (not documented).
Method: documentation only; no commands were run.
