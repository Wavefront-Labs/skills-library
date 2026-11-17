---
id: computing-software.database-administration.valkey.functions-libraries-fcall
name: functions-libraries-fcall
category: computing-software
field: database-administration
product: valkey
tags: [functions, function-load, fcall, libraries, register-function, lua, programmability]
level: practitioner
status: docs-checked
description: "Valkey Functions (7.0+): FUNCTION LOAD libraries with shebang, server.register_function, FCALL, KEYS and args, REPLACE, FUNCTION LIST, persistence and replication."
sources:
  - https://valkey.io/topics/functions-intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Functions extend the server with named, persistent code. Unlike `EVAL` scripts (ephemeral, per-application, SHA1-identified, copied to every app instance, unable to call each other), functions are database artifacts: declared before use, persisted to the AOF, replicated to replicas, and not at risk of `NOSCRIPT` aborting a transaction. For a pure cache, extra mechanisms are needed for durability. Execution is atomic and blocking like a transaction, so keep functions short. Lua 5.1 is used; the Lua debugger is unsupported.

A function lives in a library; libraries are immutable and updated as a whole, and functions in one can call shared local helpers. Source must start with a shebang naming the library:
```
#!lua name=mylib
local function my_hset(keys, args)
  local time = server.call('TIME')[1]
  return server.call('HSET', keys[1], '_last_modified_', time, unpack(args))
end
server.register_function('my_hset', my_hset)
```
Loading a library with no registered function fails with `No functions registered`. `FUNCTION LOAD` returns the library name; update with `cat mylib.lua | valkey-cli -x FUNCTION LOAD REPLACE` (without `REPLACE` an existing library is an error). Inspect with `FUNCTION LIST`, remove with `FUNCTION DELETE`.

Call: `FCALL my_hset 1 myhash myfield "some value"`. The number is the count of key-name arguments; the callback gets a `keys` table and an `args` table. All accessed keys must be passed as key arguments (standalone and cluster).

Extras: `server.setresp(3)` makes `server.call` return maps (e.g. delete a field from an `HGETALL` reply); `server.error_reply(msg)` returns an error; `server.log(server.LOG_WARNING, msg)` writes to the log.

## Checked
2026-11-03. Confirmed against the Valkey Functions page (valkey.io/topics/functions-intro/): functions versus EVAL, introduced in 7.0, persistence to the AOF and replication, atomic blocking execution, Lua 5.1 without the debugger, the shebang format, `No functions registered`, `FUNCTION LOAD ... REPLACE`, `FCALL` key counting, `server.setresp(3)`, `server.error_reply` and `server.log` (used in the page's helper example), and the all-keys-as-arguments rule. The page carries an under-review notice. Nothing removed.
Method: documentation only; no commands were run.
