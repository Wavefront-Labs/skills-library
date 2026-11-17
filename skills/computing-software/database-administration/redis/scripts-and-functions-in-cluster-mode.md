---
id: computing-software.database-administration.redis.scripts-and-functions-in-cluster-mode
name: scripts-and-functions-in-cluster-mode
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, script-keys-cluster, redis-cluster, eval, functions, hash-tags, redis-programmability]
level: practitioner
status: docs-checked
description: "Write Redis Lua scripts and Functions that work in Cluster: declare every key in KEYS, keep them in one hash slot with hash tags, and load functions on every primary."
sources:
  - https://redis.io/docs/latest/develop/interact/programmability/eval-intro/
  - https://redis.io/docs/latest/develop/interact/programmability/functions-intro/
  - https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripts and functions in cluster mode

**Goal:** scripts that run atomically in Redis Cluster without `CROSSSLOT` errors or silent wrong-node writes.

## Rules
1. **Every key the script touches must be passed in `KEYS`**, never built inside the script from `ARGV` or concatenation. The client routes by `KEYS`; Cluster checks them.
2. **All keys must map to the same hash slot.** Otherwise Cluster rejects the command with a CROSSSLOT error.
3. Use hash tags so related keys co-locate: only the part inside `{...}` is hashed.
```text
EVAL "redis.call('INCR', KEYS[1]); return redis.call('EXPIRE', KEYS[2], ARGV[1])" 2 {user:42}:count {user:42}:seen 60
```
`{user:42}:count` and `{user:42}:seen` share a slot.

## Accessing undeclared keys
The docs require every key a script accesses to be passed as an input key argument; scripts must
not build key names or derive them from stored data. A script that begins with a `#!lua` shebang
(7.0+) cannot access keys in different hash slots by default, while a script without a shebang
can, so an undeclared key may work on a standalone server and still be wrong in Cluster. The
shebang can also declare flags, for example `#!lua flags=no-writes,allow-stale`; the available
flags are listed in the Script flags section of the Lua API reference.

## Functions
```text
FUNCTION LOAD "#!lua name=ratelimit\nredis.register_function('hit', function(keys, args) ... end)"
FCALL hit 1 {user:42}:rl 10 60
```
- Functions are propagated to a node's replicas automatically and persisted in the AOF, but they are **not** shared across nodes: load them on every node. The docs suggest `redis-cli --cluster-only-masters --cluster call <host:port> FUNCTION LOAD ...`.
- `redis-cli --cluster add-node` copies the loaded functions from an existing node to the new node (per the docs); `redis-cli --functions-rdb` extracts functions from a server into an RDB file.

## EVALSHA in cluster
`SCRIPT LOAD` caches per node and the cache is volatile: a restart, a failover or `SCRIPT FLUSH` can clear it, after which `EVALSHA` returns `NOSCRIPT`. Clients should reload with `SCRIPT LOAD` and retry (most libraries do), or use plain `EVAL` in pipelines.

## Hot-slot risk
Hash tags concentrate keys; a tag per tenant with one giant tenant creates a hot shard. Tag by the smallest unit that the script needs atomically.

## Verify
`CLUSTER KEYSLOT {user:42}:count` equals `CLUSTER KEYSLOT {user:42}:seen`; `FUNCTION LIST` on each primary returns the library.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the scripting pages: every key a script accesses must be passed as an input key argument (never built in the script); scripts with a `#!lua` shebang (7.0+) cannot access keys in different slots by default while scripts without one can; shebang flags example `#!lua flags=no-writes,allow-stale`; SCRIPT LOAD / EVALSHA / NOSCRIPT behaviour and the volatile script cache; function libraries need `#!<engine> name=<library>`, FCALL takes numkeys then keys then args, functions replicate to replicas and persist in the AOF but must be loaded on all cluster nodes, add-node copies them. Confirmed hash tag rule and that multi-key commands need one slot from the cluster specification. Removed unconfirmed: the exact CROSSSLOT message, undeclared-key detection claim, `allow-cross-slot-keys` mention, FUNCTION DUMP/RESTORE and the REPLACE option.
Method: documentation only; no commands were run.
