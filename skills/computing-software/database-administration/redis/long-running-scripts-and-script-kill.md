---
id: computing-software.database-administration.redis.long-running-scripts-and-script-kill
name: long-running-scripts-and-script-kill
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, lua, script-kill, function-kill, busy, busy-reply-threshold, lua-time-limit, shutdown-nosave]
level: practitioner
status: docs-checked
description: "Handle Redis BUSY errors from slow Lua scripts or functions: busy-reply-threshold, SCRIPT KILL / FUNCTION KILL limits, SHUTDOWN NOSAVE, and writing scripts that stay short."
sources:
  - https://redis.io/docs/latest/develop/programmability/
  - https://redis.io/docs/latest/commands/script-kill/
  - https://redis.io/docs/latest/develop/programmability/lua-api/
  - https://raw.githubusercontent.com/redis/redis/unstable/src/script.c
  - https://raw.githubusercontent.com/redis/redis/unstable/src/server.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-running scripts (BUSY, SCRIPT KILL, FUNCTION KILL)

A Lua script or function runs **atomically**: while it runs, Redis serves no other command.

## What happens when it runs long
Scripts have a maximum execution time, `busy-reply-threshold` (default 5000 ms, settable with `CONFIG SET`; old name
`lua-time-limit`). When it is exceeded Redis does not stop the script: it logs a warning and starts replying
to other clients with a BUSY error. Only `SCRIPT KILL`, `FUNCTION KILL` and `SHUTDOWN NOSAVE` are accepted meanwhile.
```
(error) BUSY Redis is busy running a script. You can only call SCRIPT KILL or SHUTDOWN NOSAVE.
```
(For a function the message names `FUNCTION KILL` instead.) Other clients keep getting BUSY until the script finishes or is stopped.

## Killing it
```
SCRIPT KILL         # for EVAL/EVALSHA scripts
FUNCTION KILL       # for functions (FCALL)
```
These only work if the script **has not performed any write** yet; killing a script that wrote would break atomicity:
```
(error) UNKILLABLE Sorry the script already executed write commands against the dataset.
You can either wait the script termination or kill the server in a hard way using the SHUTDOWN NOSAVE command.
```
Then the choices are: wait for it to finish, or `SHUTDOWN NOSAVE`, which stops the server without saving the dataset
(the in-memory data, including the script's partial writes, is abandoned; recovery is from the last RDB/AOF).
With effects replication the script's write commands are wrapped in MULTI/EXEC and sent to replicas and the AOF
when the script finishes. A script that was sent by a master over replication cannot be killed on the replica.

## Write scripts that stay short
- Bound loops: never iterate an entire large collection (`SMEMBERS`, `HGETALL` of huge keys)
  or the keyspace inside a script; page through from the client with SCAN and call the
  script per batch.
- Keep heavy computation in the application; scripts should do small atomic read-modify-write.
- Declare all keys as key arguments (required for cluster routing).
- Read-only scripts: `EVAL_RO` / `FCALL_RO`, or the `no-writes` flag, can run on replicas, can always be killed with
  `SCRIPT KILL`, and are not blocked by OOM.
- Flag functions `no-writes` where possible so they can always be stopped.

## Detect slow scripts
`SLOWLOG GET` shows `EVALSHA`/`FCALL` entries with durations; `INFO commandstats`
(`cmdstat_evalsha ... usec_per_call`); `LATENCY LATEST` event `command`.

## Verify
In a test instance, run a deliberately long read-only script: other clients get BUSY after the
threshold and `SCRIPT KILL` restores service; production scripts show sub-millisecond durations
in `INFO commandstats`.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): programmability overview
(maximum execution time, read-only scripts), SCRIPT KILL, Lua API reference, INFO, plus `src/script.c`,
`src/server.c` and `src/config.c` from the redis/redis repository. Confirmed: `busy-reply-threshold` default 5000 and the
`lua-time-limit` alias, which commands are accepted while BUSY, the SCRIPT KILL / FUNCTION KILL read-only limit,
the exact BUSY text for scripts and functions, the UNKILLABLE texts, `SHUTDOWN NOSAVE`, read-only script
properties, MULTI/EXEC wrapping of effects. Removed: "Replicas and Sentinel see the master as unresponsive, which can
trigger a failover" and "the partial writes never reached the AOF" as stated facts (not documented), and the
`redis.setresp(3)` advice (unrelated to execution time).
Method: documentation only; no commands were run.
