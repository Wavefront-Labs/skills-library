---
id: computing-software.database-administration.redis.cluster-creation-and-management-with-redis-cli
name: cluster-creation-and-management-with-redis-cli
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-cluster, redis-cli-cluster, cluster-create, cluster-reshard, cluster-rebalance, add-node, cluster-check, cluster-replicas, cluster-add-node]
level: practitioner
status: docs-checked
description: "Create and operate a Redis Cluster with redis-cli --cluster: create with replicas, check/fix, add and remove nodes, reshard and rebalance slots safely."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Creating and managing a cluster with redis-cli --cluster

**Goal:** stand up a sharded Redis Cluster and change its shape without downtime.

## Node config (each node)
```text
port 7000
cluster-enabled yes
cluster-config-file nodes-7000.conf     # managed by Redis, do not edit
cluster-node-timeout 5000
appendonly yes
cluster-require-full-coverage no        # keep serving healthy slots if some are down
```
Open the client port and the cluster bus port (port + 10000).

## Create (3 primaries + 1 replica each)
```bash
redis-cli -a "$PW" --cluster create 10.0.0.1:7000 10.0.0.2:7000 10.0.0.3:7000 \
  10.0.0.4:7000 10.0.0.5:7000 10.0.0.6:7000 --cluster-replicas 1
```
Check the result with:
```bash
redis-cli -a "$PW" --cluster check 10.0.0.1:7000      # slot coverage, open slots, agreement
redis-cli -a "$PW" -c -h 10.0.0.1 -p 7000 cluster nodes
```

## Add capacity
```bash
redis-cli --cluster add-node 10.0.0.7:7000 10.0.0.1:7000                 # empty primary
redis-cli --cluster add-node 10.0.0.8:7000 10.0.0.1:7000 --cluster-slave --cluster-master-id <id-of-7>
redis-cli --cluster rebalance 10.0.0.1:7000 --cluster-use-empty-masters  # move slots to it
redis-cli --cluster reshard 10.0.0.1:7000 --cluster-from <src-id> --cluster-to <dst-id> --cluster-slots 1000 --cluster-yes
```
Resharding runs while the cluster serves traffic; clients follow redirects during the move.

## Remove a node
Reshard all its slots away first (`rebalance --cluster-weight <id>=0`), then:
```bash
redis-cli --cluster del-node 10.0.0.1:7000 <node-id>
```

## Repair
`redis-cli --cluster fix 10.0.0.1:7000` closes slots stuck in importing/migrating after an interrupted reshard. Manual failover from a replica: `CLUSTER FAILOVER` (on the replica).

## Gotchas
- Large keys make slot migration slow; find them first with `redis-cli --bigkeys`.
- Multi-key commands need keys in one slot: use hash tags `{user:42}:cart`.
- The cluster bus port defaults to the client port + 10000 and can be overridden with `cluster-port`.

## Verify
`--cluster check` reports `[OK] All 16384 slots covered` and `cluster nodes` shows at least one replica per primary.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed against the Redis Cluster scaling page and redis-cli.c: `--cluster create ... --cluster-replicas 1`, `check`, `fix`, `add-node` with `--cluster-slave` and `--cluster-master-id`, `del-node`, `call`, `reshard` with `--cluster-from/--cluster-to/--cluster-slots/--cluster-yes`, `rebalance` with `--cluster-weight` and `--cluster-use-empty-masters`; the `[OK] All 16384 slots covered` message; bus port = client port + 10000 (`cluster-port` overrides); `cluster-require-full-coverage` default yes. Removed unconfirmed: replica placement by redis-cli, MIGRATE atomicity, announce-ip advice.
Method: documentation only; no commands were run.
