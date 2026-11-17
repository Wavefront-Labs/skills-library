---
id: computing-software.database-administration.redis.cluster-sentinel-and-failover
name: cluster-sentinel-and-failover
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-sentinel, redis-cluster, failover, split-brain, quorum, resharding, hash-slot, cross-slot, client-side-caching, topology]
level: advanced
status: docs-checked
description: "Run Redis Sentinel or Cluster for HA, size quorum correctly, and diagnose resharding stalls and multi-key cross-slot failures."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis Sentinel and Cluster — quorum, resharding, and multi-key limits

**Goal:** choose Sentinel vs. Cluster for the right reason, size quorum so a
network blip doesn't trigger an unwanted failover, and know which commands simply
don't work across a sharded keyspace.

## 1. Sentinel: HA for a single primary/replica set, no sharding
Sentinels monitor a primary and its replicas, agree that the primary is down, and promote
a replica. `quorum` (the last argument of `sentinel monitor`) is the number of Sentinels that
must agree the primary is unreachable, but the quorum is only used to detect the failure: to
start a failover one Sentinel must be authorised by the **majority** of all Sentinels, so no
failover starts in a minority partition. Deploy at least three Sentinels on machines that fail
independently (different servers or availability zones). A quorum below the majority makes
Sentinel more sensitive to primary failures; a quorum above it needs more Sentinels reachable
before it acts.

## 2. The split-brain window Sentinel doesn't fully prevent
If the old primary becomes reachable again after a replica was already promoted
(network partition healed), writes may have landed on both for a window.
`min-replicas-to-write` on the primary (refuse writes if fewer than N replicas are
connected within `min-replicas-max-lag` seconds) restricts the window but there is always a
window for data loss: replication is asynchronous, so acknowledged writes can be lost at
failover. Design the application to tolerate this.

## 3. Cluster: sharding across 16384 hash slots
Keys map to one of 16384 slots (`CRC16(key) mod 16384`); slots are assigned to shards (primary +
replicas each). Client-side (cluster-aware client) or server-side (`-ASK`/`-MOVED`
redirects) routing finds the right node. Resharding moves slots between nodes
live (`redis-cli --cluster reshard`); `redis-cli --cluster fix` repairs slots left open by an interrupted move.

## 4. Multi-key operations: the cross-slot wall
Multi-key commands such as `MSET` and `MGET` work only when every key hashes to the
same slot (the server otherwise returns a CROSSSLOT error). Scripts that start with a
`#!lua` shebang cannot access keys in different slots by default. Use **hash tags** — `{user:1000}.profile` and `{user:1000}.sessions` both
hash on `user:1000` (the part inside `{}`) — to deliberately co-locate related
keys on one slot when atomic multi-key operations are needed. Code that ran on a
single node can break on Cluster if its key naming ignores this.

## 5. Cluster failover mechanics
Each primary's replicas run their own mini-election (similar quorum logic to
Sentinel) when their primary is unreachable for `cluster-node-timeout`. A cluster
with no replica for a given primary has no automatic failover for that shard's
slots — losing that one node makes its slots unavailable until manual
intervention (`CLUSTER FAILOVER` forced, or replacing the node). Every primary
needs at least one replica if HA matters, checked per-shard, not just "the cluster
has replicas somewhere."

## Verify
- [ ] Sentinel quorum is a true majority of an odd Sentinel count, spread across failure domains.
- [ ] `min-replicas-to-write` is set if dual-write exposure during partition is unacceptable.
- [ ] Every Cluster shard (not just the cluster as a whole) has at least one replica.
- [ ] Multi-key commands in application code were audited for cross-slot usage and hash-tagged where atomicity is required.
- [ ] A resharding operation has been tested under write load, not just at rest.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed: Sentinel quorum only detects the failure while a majority of Sentinels must authorise the failover (no failover in a minority partition), at least three Sentinels on independently failing machines, quorum below or above the majority trade-offs; `min-replicas-to-write` and `min-replicas-max-lag` bound but do not remove the data-loss window (replication is asynchronous); `CRC16(key) mod 16384`, hash tag rule; replica failover after `cluster-node-timeout`; `CLUSTER FAILOVER` FORCE and TAKEOVER. Rewrote the muddled quorum paragraph and removed unconfirmed throttling claims about resharding.
Method: documentation only; no commands were run.
