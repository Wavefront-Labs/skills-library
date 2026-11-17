---
id: computing-software.database-administration.redis.debugging-lua-with-redis-ldb
name: debugging-lua-with-redis-ldb
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, lua, ldb, redis-cli, debugging, script-debug, eval, breakpoint]
level: practitioner
status: docs-checked
description: "Debug Redis EVAL Lua scripts step by step with redis-cli --ldb: breakpoints, print, redis commands, forked vs sync mode, and the safety rules."
sources:
  - https://redis.io/docs/latest/develop/programmability/lua-debugging/
  - https://redis.io/docs/latest/develop/programmability/lua-api/
  - https://redis.io/docs/latest/commands/script-debug/
  - https://redis.io/docs/latest/develop/tools/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Lua with redis-cli --ldb

**Goal:** step through an `EVAL` script, inspect variables and Redis replies, instead of printf debugging with `redis.log`. Use a development server: the documentation says to avoid debugging on production.

## Start a session
```bash
redis-cli --ldb --eval ./ratelimit.lua rl:user:42 , 10 60
```
Key names come before the comma, arguments after it, each as a separate command-line argument. By default a session is **forked**: the server does not block, and all changes are rolled back when the session ends, so you can restart from the same data. `--ldb-sync-mode` (or `SCRIPT DEBUG SYNC`) debugs in the main process: the server is blocked for the whole session and the changes are kept.

## Commands inside the debugger
```text
s / step / n    execute current line and stop again
c / continue    run to next breakpoint
l / list        show source around current line
p / print       print all locals, or `p varname` (also KEYS and ARGV)
b 12            breakpoint at line 12; `b -12` removes it; `b 0` removes all; `b` lists them
t / trace       show a backtrace
r / redis       run a Redis command: `r GET rl:user:42`
e / eval        run Lua code (outside the current call frame)
w / whole       list all source code
a / abort       stop the script (in sync mode the changes so far are kept)
m / maxlen      trim logged replies and variable dumps; 0 means unlimited
restart         reload the script file and start over (handled by redis-cli)
quit            end the session and exit redis-cli
```
The debugger starts in stepping mode, stopping at the first line that does something.

## In-script hooks
```lua
redis.breakpoint()          -- stop as if there were a breakpoint on the next line
redis.debug("count", c)     -- print to the debugger console; no effect outside a debugging session
```
Both are available in EVAL scripts only, not in functions. Remove them before shipping. A breakpoint on a line Lua never executes (a `local` declaration or a comment) never triggers.

## Gotchas
- Functions (`FUNCTION LOAD`) cannot be debugged with LDB: the Lua API lists `redis.breakpoint` and `redis.debug` as unavailable in functions. Copy the body into an EVAL script to debug it.
- `SCRIPT DEBUG YES|SYNC|NO` is the server command behind it: `YES` is the forked, rolled-back mode, `SYNC` blocks and keeps changes, `NO` turns debug mode off. It applies to scripts run with `EVAL`.
- Forked debugging on a large production dataset is still a risk; use a local copy or staging restored from RDB.

## Verify
Step to the line that computes the result and `p` the value; confirm the final reply matches expectations and that forked mode left the dataset unchanged (`GET` the key after the session).

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): Lua debugging page, Lua API
reference, SCRIPT DEBUG, redis-cli reference. Confirmed: `--ldb`, `--ldb-sync-mode`, `--eval` key/argument
syntax, the debugger help screen, forked-versus-sync behaviour, `quit`/`restart`, `redis.breakpoint` and
`redis.debug`, availability in functions (none), `SCRIPT DEBUG` modes. Fixed: both source URLs used
`/develop/interact/programmability/`, which is 404; they are now under `/develop/programmability/`.
Removed: the claim that `redis.breakpoint()` is a no-op outside a session (only `redis.debug` is documented that way),
and the claim that ldb "issues SCRIPT DEBUG under the hood" was reworded to the documented relationship.
Method: documentation only; no commands were run.
