---
id: computing-software.database-administration.redis.functions-with-function-load
name: functions-with-function-load
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, functions, function-load, fcall, lua, libraries, scripting, replication]
level: practitioner
status: docs-checked
description: "Package server-side Redis logic as Functions: FUNCTION LOAD libraries, FCALL/FCALL_RO, flags, replication and cluster loading, versus EVAL scripts."
sources:
  - https://redis.io/docs/latest/develop/programmability/functions-intro/
  - https://redis.io/docs/latest/commands/function-list/
  - https://redis.io/docs/latest/commands/function-restore/
  - https://redis.io/docs/latest/commands/function-stats/
  - https://redis.io/docs/latest/develop/programmability/lua-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions with FUNCTION LOAD (7.0+)

**Goal:** server-side logic that is named, persisted with the data and replicated, instead of ad-hoc EVAL scripts.

## Library
```lua
#!lua name=ratelimit
local function allow(keys, args)
  local n = redis.call('INCR', keys[1])
  if n == 1 then redis.call('EXPIRE', keys[1], args[2]) end
  return n <= tonumber(args[1]) and 1 or 0
end
local function remaining(keys, args)
  local n = tonumber(redis.call('GET', keys[1]) or '0')
  return math.max(0, tonumber(args[1]) - n)
end
redis.register_function('rl_allow', allow)
redis.register_function{ function_name = 'rl_remaining', callback = remaining, flags = { 'no-writes' } }
```
```bash
cat ratelimit.lua | redis-cli -x FUNCTION LOAD REPLACE
redis-cli FCALL rl_allow 1 rl:user:42 100 60
redis-cli FCALL_RO rl_remaining 1 rl:user:42 100     # allowed on replicas because of no-writes
```
The first line (`#!<engine> name=<library>`) is mandatory, and a library must register at least one function. The Lua engine runs
the library source at load time, which is when `redis.register_function` is called. Functions receive the key
names and the other arguments as two Lua tables (`keys`, `args`), not through `KEYS`/`ARGV`.

## Manage
```text
FUNCTION LIST LIBRARYNAME ratelimit WITHCODE
FUNCTION DELETE ratelimit
FUNCTION STATS             # running function (name, command, duration_ms) and per-engine counts
FUNCTION KILL              # only if it has not written
FUNCTION DUMP / FUNCTION RESTORE <payload> [FLUSH | APPEND | REPLACE]   # move libraries between servers
```
`FUNCTION RESTORE` defaults to `APPEND` (abort on a library name collision); `REPLACE` overwrites libraries with the
same name, `FLUSH` deletes all existing libraries first. Functions are persisted in the AOF and replicated from
master to replicas, so failover keeps them. `FLUSHALL` does not delete functions.

In Redis Cluster, replication does not cover other shards: load the library on every master, for example
`redis-cli --cluster-only-masters --cluster call host:port FUNCTION LOAD ...`; `redis-cli --cluster add-node`
copies loaded functions to the new node. For an ephemeral cache, `redis-cli --functions-rdb <file>` extracts only
the functions into an RDB file that Redis can load at startup.

## Deploying
- Keep libraries in git; deploy with `FUNCTION LOAD REPLACE`. A library is replaced as a whole, with all its
  functions, in one operation (you cannot update single functions).
- Version in the library name or function names when changing signatures (`rl_allow_v2`) so old app instances keep working during rollout.
- Flags: `no-writes`, `allow-oom`, `allow-stale`, `no-cluster`, `allow-cross-slot-keys`. Without flags Redis assumes the function may read and write, so `FCALL_RO` and replicas reject it.

## Same rules as scripts
All key names the function accesses must be passed as key arguments, same-slot keys in Cluster, atomic execution
blocks the server so keep functions short, and `busy-reply-threshold` applies (`FUNCTION KILL` stops a function that has not written).
The Lua debugger (LDB) does not support functions.

## Verify
`FUNCTION LIST` on a replica shows the library after loading on the primary; after a failover `FCALL rl_allow` still works.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): Redis functions page, FUNCTION LIST,
FUNCTION RESTORE, FUNCTION STATS, Lua API reference (flags, `redis.register_function`), programmability overview,
FLUSHALL. Confirmed: shebang format, `REPLACE`, `FCALL`/`FCALL_RO` and `no-writes`, flag names, persistence and replication
of libraries, cluster loading command and `add-node` behaviour, `--functions-rdb`, RESTORE policies and default, STATS
fields, `FLUSHALL` leaves functions, LDB exception. Fixed: the cluster loading command is
`redis-cli --cluster-only-masters --cluster call ... FUNCTION LOAD` (the old text omitted the option); the grammar order
is `FUNCTION LIST [LIBRARYNAME pattern] [WITHCODE]`.
Method: documentation only; no commands were run.
