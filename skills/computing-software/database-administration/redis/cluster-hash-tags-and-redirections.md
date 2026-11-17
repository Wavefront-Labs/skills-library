---
id: computing-software.database-administration.redis.cluster-hash-tags-and-redirections
name: cluster-hash-tags-and-redirections
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-cluster, hash-tags, crossslot, moved, ask, keyslot, multi-key]
level: practitioner
status: docs-checked
description: "Design Redis Cluster key names with hash tags to avoid CROSSSLOT errors, and read MOVED/ASK redirections correctly in clients and logs."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
  - https://redis.io/docs/latest/develop/using-commands/multi-key-operations/
  - https://redis.io/docs/latest/commands/spublish/
  - https://raw.githubusercontent.com/redis/redis/unstable/src/cluster.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash tags and redirections in Redis Cluster

## Slots
The key space is split into 16384 hash slots (`CRC16(key) mod 16384`). Each master serves a subset of the slots.
```
CLUSTER KEYSLOT user:1001
```

## CROSSSLOT
Multi-key operations must have **all keys in the same slot**. The Redis multi-key reference lists the single-slot
commands in a cluster: `MSETNX`, `RENAME`, `COPY`, `LMOVE`, `SINTERSTORE`, `SUNIONSTORE`, `ZUNIONSTORE`, `BITOP`,
`PFMERGE` and others. Keys in a `MULTI/EXEC` transaction or in a Lua script must also share a slot. With a standard
cluster-aware client (the OSS cluster API), `MGET`, `MSET`, `DEL`, `UNLINK` and pipelines are single-slot too.
```
(error) CROSSSLOT Keys in request don't hash to the same slot
```
Script flags: a script or function can opt out with `allow-cross-slot-keys`, but declared keys must still share one slot.

## Hash tags
If a key contains `{...}`, only the substring between the **first** `{` and the first `}` to its right is hashed,
provided it is not empty:
```
user:{1001}:profile
user:{1001}:cart
user:{1001}:sessions
```
All three land in the same slot, so `MULTI ... EXEC` or a script over them works.
Rules from the specification: `foo{}{bar}` hashes the whole key (empty braces); `foo{{bar}}zap` hashes `{bar`;
`foo{bar}{zap}` hashes `bar`. A key that starts with `{}` is always hashed whole.

Design trade-off: everything sharing a tag lives on one node. Tag by a high-cardinality entity
(user id, tenant id for small tenants), never by a constant like `{global}` or you create a hot
shard. Large tenants may need their own key spread.

## MOVED and ASK
- `-MOVED 3999 10.0.1.12:6379`: the slot is served by another node (the endpoint may be empty, meaning "same host, this port").
  Cluster-aware clients update their slot map and retry; many MOVED errors in app logs mean the client is not
  caching the map (or a resharding just happened).
- `-ASK 3999 10.0.1.12:6379`: the slot is being migrated; this key may already be on the target.
  The client sends `ASKING`, then the command, to the target, without updating its map. A node whose slot is
  IMPORTING only accepts queries for it after `ASKING`.
- During resharding, multi-key operations on keys that do not exist yet or that are split between source and
  target return `-TRYAGAIN`; retry later.
`redis-cli -c` follows redirections for you.

## Other cluster rules
- Only database 0 exists (`SELECT` is not allowed).
- `KEYS`, `SCAN`, `DBSIZE`, `FLUSHALL` and `FLUSHDB` act on the current shard only in an open source cluster:
  run them on every master. Since Redis 8.0, `KEYS`, `SCAN` and `SORT` with a pattern that begins with a hash tag
  (for example `SCAN 0 MATCH {abc}*`) search only that slot.
- Pub/Sub: sharded pub/sub (`SPUBLISH`/`SSUBSCRIBE`, 7.0+) assigns shard channels to slots with the same
  algorithm as keys, so a shard message goes to the node owning the slot and is forwarded within that shard.
- Scripts must declare every key in `KEYS[]` (not build names dynamically) so the cluster can route them.

## Verify
`CLUSTER KEYSLOT` returns the same slot for all keys of an entity; transactional code paths
run without CROSSSLOT errors against a test cluster; client metrics show few MOVED redirections
outside resharding windows.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): cluster specification, multi-key
operations, SPUBLISH, plus `src/cluster.c` from the redis/redis repository. Confirmed: 16384 slots, hash tag
algorithm and its examples, CROSSSLOT/MOVED/ASK/TRYAGAIN formats and behaviour, `ASKING` for IMPORTING slots,
single-slot command table, database 0 only, per-shard KEYS/SCAN/FLUSHALL, 8.0 single-slot pattern optimisation,
sharded pub/sub since 7.0.0, script flag `allow-cross-slot-keys`.
Fixed: the claim that classic `PUBLISH` is "broadcast cluster-wide (bandwidth)" was not confirmed and was removed;
MOVED is not only "permanent" (the spec describes it as the slot served by another node).
Method: documentation only; no commands were run.
