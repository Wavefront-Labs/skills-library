---
id: computing-software.database-administration.redis.cluster-node-timeout-and-full-coverage
name: cluster-node-timeout-and-full-coverage
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-cluster, cluster-node-timeout, cluster-require-full-coverage, failover, clusterdown, availability]
level: practitioner
status: docs-checked
description: "Tune Redis Cluster failure detection (cluster-node-timeout, replica validity factor) and decide between full-coverage and partial availability when slots are lost."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
  - https://raw.githubusercontent.com/redis/redis/unstable/src/config.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster-node-timeout and cluster-require-full-coverage

## cluster-node-timeout (default 15000 ms)
- The maximum time a node can be unavailable without being considered failing. A node is flagged `PFAIL`
  once unreachable for more than this long; it becomes `FAIL` when a majority of masters report `PFAIL` or
  `FAIL` for it within twice the timeout, and its replicas can then be promoted.
- A replica waits before asking for election: 500 ms + a random 0-500 ms + 1000 ms per replica rank (rank 0
  is the replica with the most replication data), counted from the moment the master is in `FAIL` state.
- Lower values (for example 5000) fail over faster; too low and GC pauses, VM steal or a long `BGSAVE` fork can
  trigger false failovers. The spec also notes that a small timeout with many nodes increases cluster bus traffic.
- Every node that cannot reach the majority of masters for the timeout stops accepting queries, which limits
  how long a minority-partition master takes writes that will later be lost.
- `cluster-replica-validity-factor` (default 10; old name `cluster-slave-validity-factor`): a replica that has been
  disconnected from its master for longer than `timeout * factor` does not try to fail over. `0` means a replica
  always tries. Any non-zero value can leave the cluster unavailable after a master failure if no replica is
  eligible, until the old master rejoins.

## cluster-require-full-coverage (default yes)
- `yes`: if some part of the key space (any hash slot) is not covered by a working node, the nodes stop accepting
  queries and clients get `-CLUSTERDOWN The cluster is down`.
- `no`: the cluster keeps serving queries for the slots that are covered; only requests for the lost slots fail.

Choose `no` when the application can tolerate partial unavailability (caches, independent tenants); keep `yes` when partial results would be wrong (multi-key consistency expectations, counting).

## cluster-allow-reads-when-down (default no)
`no`: a node stops serving all traffic when the cluster is marked failed (it cannot reach a quorum of masters or
full coverage is not met), so it never reads data it may not know to be stale. `yes` lets nodes serve reads in that
state (clients then see `-CLUSTERDOWN The cluster is down and only accepts read commands` for writes); stale data
is possible. Useful for read-mostly caches during incidents.

## Apply
All three settings (and the validity factor) can be changed at runtime with `CONFIG SET`:
```text
CONFIG SET cluster-node-timeout 5000
CONFIG SET cluster-require-full-coverage no
CONFIG REWRITE
```
Set the same values on every node (for example `redis-cli --cluster call <node>:<port> CONFIG SET ...`).

## Verify
In staging kill a primary and its replica together: with `no`, keys in other slots still work; with `yes`,
every request gets CLUSTERDOWN.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): "Scale with Redis Cluster"
(configuration parameters), cluster specification (failure detection, replica rank), plus `redis.conf` and
`src/config.c` from the redis/redis repository, and the CLUSTERDOWN strings in `src/cluster.c`. Confirmed:
default values (15000, 10, yes, no), CONFIG SET support for the four settings, PFAIL/FAIL rules, replica delay
formula, quorum behaviour, error texts. Fixed: a minority-side master stops accepting queries, not only writes;
"failover is about timeout + 1-2 s" was removed (the delay is 500 ms + 0-500 ms random + 1 s per rank after FAIL);
the "6.0+" version tag on `cluster-allow-reads-when-down` was removed because no source states it.
Method: documentation only; no commands were run.
