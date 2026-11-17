---
id: computing-software.database-administration.redis.eval-and-evalsha-lua-scripts
name: eval-and-evalsha-lua-scripts
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, lua, eval, evalsha, scripting, script-load, noscript, atomicity, cluster-keys]
level: practitioner
status: docs-checked
description: "Write atomic Redis Lua scripts with KEYS/ARGV, cache them with SCRIPT LOAD/EVALSHA, handle NOSCRIPT, and avoid cluster and replication pitfalls."
sources:
  - https://redis.io/docs/latest/develop/programmability/eval-intro/
  - https://redis.io/docs/latest/develop/programmability/lua-api/
  - https://redis.io/docs/latest/develop/programmability/
  - https://redis.io/docs/latest/commands/evalsha_ro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EVAL / EVALSHA scripts

**Goal:** atomic read-modify-write logic in one round trip, cached on the server and safe in Cluster.

## Write the script with KEYS and ARGV
```lua
-- rate limit: allow ARGV[1] requests per ARGV[2] seconds
local current = redis.call('INCR', KEYS[1])
if current == 1 then redis.call('EXPIRE', KEYS[1], ARGV[2]) end
if current > tonumber(ARGV[1]) then return 0 end
return 1
```
```text
EVAL "<script>" 1 rl:user:42 100 60
```
Every key the script accesses must be passed as a key argument (it becomes `KEYS`), so standalone and clustered
deployments both work; never access keys with programmatically built names or names read from stored data. Pass
everything else as `ARGV`. Scripts cannot declare global variables: use `local`.

## Cache and call by SHA
```text
SCRIPT LOAD "<script>"            # compiles and caches without running; returns the sha1
EVALSHA 3c4e... 1 rl:user:42 100 60
EVALSHA_RO ...                    # 7.0+: read-only variant (also EVAL_RO)
```
The script cache is volatile: it is not persisted and may be cleared on a server restart, on failover to a
replica, or by `SCRIPT FLUSH`. A missing script returns `(error) NOSCRIPT No matching script`: load it with
`SCRIPT LOAD` and call `EVALSHA` again (most clients do this for you). Inside a pipeline the NOSCRIPT error cannot be
handled mid-flight, so clients fall back to plain parameterized `EVAL` there; `SCRIPT LOAD` first guarantees
`EVALSHA` will not fail.

## Semantics
- Atomic: while a script runs, all server activity is blocked.
- `redis.call` raises a runtime error back to the caller; `redis.pcall` returns the error to the script as a table
  with an `err` field so it can be handled.
- Replication sends the script's write commands (effects replication, wrapped in MULTI/EXEC), not the script.
  This has been the default since 5.0 and the only mode since 7.0, so scripts no longer need to be deterministic.
- Long scripts: after `busy-reply-threshold` (default 5000 ms; older name `lua-time-limit`) Redis answers other
  clients with BUSY; `SCRIPT KILL` works only if the script has not written, otherwise `SHUTDOWN NOSAVE`.
- Under `maxmemory`, the first write command that uses extra memory aborts the script (unless called with
  `redis.pcall`), unless the script has the `allow-oom` or `no-writes` flag.
- `#!lua flags=no-writes,allow-stale` on the first line declares flags (7.0+); a script with `#!` cannot touch keys
  in different cluster slots unless it also has `allow-cross-slot-keys`.

## Cluster
All keys a script touches must hash to the same slot: use hash tags (`{user:42}:a`, `{user:42}:b`).

## Prefer Functions for shared logic (7.0+)
Functions are named, persisted with the dataset and replicated, so they avoid the NOSCRIPT dance.

## Gotchas
- Generating script text dynamically (different literals each time) fills the script cache: pass values as ARGV.
  Inspect `INFO` fields `number_of_cached_scripts` and `used_memory_scripts`.
- Number conversion: a Lua number returned to the client becomes an integer reply (the fractional part is dropped),
  so return floats as strings. A Lua `false` becomes a nil reply and a table stops at the first `nil`.

## Verify
`SCRIPT EXISTS <sha>` returns 1 after load; a concurrent load test of the rate limiter never exceeds the limit.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): Scripting with Lua, Lua API reference,
programmability overview, EVALSHA_RO, INFO. Confirmed: KEYS/ARGV rules, SCRIPT LOAD/EVALSHA/NOSCRIPT behaviour and
the pipelining caveat, `redis.call` versus `redis.pcall`, effects replication (default 5.0, only mode 7.0),
`busy-reply-threshold` default and old name (config.c), SCRIPT KILL limits, low-memory behaviour, shebang flags,
Lua-to-RESP2 number conversion, `EVALSHA_RO` since 7.0.0. Fixed: both `/develop/interact/programmability/` URLs
were 404 (now `/develop/programmability/`); "cache not guaranteed to be replicated to new replicas" was replaced
by the documented "may be cleared on restart, failover or SCRIPT FLUSH"; NOSCRIPT recovery is SCRIPT LOAD then
EVALSHA (EVAL only inside pipelines); "scripts should be deterministic" is obsolete since 7.0.
Removed: "no rollback" wording for `redis.call` errors (the pages state atomicity, not rollback).
Method: documentation only; no commands were run.
