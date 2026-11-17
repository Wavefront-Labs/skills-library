---
id: computing-software.database-administration.redis.cluster-manual-failover-and-replica-migration
name: cluster-manual-failover-and-replica-migration
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, cluster-failover, replica-migration, redis-cluster, redis-ha, cluster-replicate]
level: practitioner
status: docs-checked
description: "Perform planned Redis Cluster switchovers with CLUSTER FAILOVER (default, FORCE, TAKEOVER), move replicas with CLUSTER REPLICATE, and tune automatic replica migration."
sources:
  - https://redis.io/docs/latest/commands/cluster-failover/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster manual failover and replica migration

**Goal:** promote a replica on purpose (patching the primary's host) with no lost writes, and keep every primary covered by a replica.

## Manual failover (run on the replica)
```text
redis-cli -h 10.0.0.12 -p 7001 CLUSTER FAILOVER
```
Default mode is safe: the primary stops accepting client writes, the replica catches up to the primary's replication offset, then switches roles and the cluster config epoch bumps. The old primary unblocks its clients and redirects them to the new primary.

| Option | Use |
|---|---|
| (none) | Planned switchover, primary reachable: no data loss |
| `FORCE` | Primary unreachable, but a majority of primaries is available to authorise the promotion |
| `TAKEOVER` | No majority (e.g. whole DC lost): replica takes over unilaterally with a new epoch; risk of conflicting configs; last resort |

Check: `CLUSTER NODES` on any node shows the old replica as `master` and the old primary as `slave`.

## Moving a replica to another primary
```text
redis-cli -h 10.0.0.15 -p 7005 CLUSTER REPLICATE <target-primary-node-id>
```
The node becomes a replica of the target primary and resyncs from it.

## Automatic replica migration
- `cluster-migration-barrier 1` (default): a replica migrates to an orphaned primary (no working replicas) only if its own primary keeps at least 1 other replica.
- `cluster-allow-replica-migration yes` (default) enables or disables the behaviour.
- Replica migration moves a replica to a primary that has no working replica.

## Gotchas
- Run manual failover on the **replica**, not the primary.
- Primary and replica on the same host or rack defeats failover; check placement with `CLUSTER NODES`.
- After switchover, run the original primary as a replica until patching is complete; fail back with another `CLUSTER FAILOVER` if placement matters.

## Verify
`redis-cli --cluster check <node>` reports all 16384 slots covered and each primary has ≥ 1 replica.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the CLUSTER FAILOVER page: it runs on a replica; the default handshake (primary stops clients, replica catches up to the offset, majority of primaries grant the epoch); FORCE needs a majority of primaries; TAKEOVER needs none and can conflict with epoch rules. Confirmed from the cluster specification: replica migration to orphaned primaries and `cluster-migration-barrier`; redis.conf 8.2: `cluster-migration-barrier` 1 and `cluster-allow-replica-migration` yes by default. Removed unconfirmed: data drop on CLUSTER REPLICATE, spare-replica advice.
Method: documentation only; no commands were run.
