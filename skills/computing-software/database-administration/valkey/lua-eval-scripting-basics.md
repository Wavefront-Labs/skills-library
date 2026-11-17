---
id: computing-software.database-administration.valkey.lua-eval-scripting-basics
name: lua-eval-scripting-basics
category: computing-software
field: database-administration
product: valkey
tags: [eval, lua, scripting, keys, argv, server-call, server-pcall, atomic, effects-replication]
level: practitioner
status: docs-checked
description: "Valkey Lua scripting with EVAL: atomic execution, KEYS and ARGV parameterisation, server.call vs server.pcall, key-access rules and effects replication."
sources:
  - https://valkey.io/topics/eval-intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Valkey runs Lua 5.1 scripts on the server. Scripts are atomic: all other server activity is blocked while one runs, so effects have either not happened or all have. Benefits: logic next to data (less latency and network), atomic multi-key and multi-type conditional updates, and custom capabilities. Eval scripts are treated as part of the client application: not named, versioned or persisted, so apps must be ready to reload them. (Functions, from 7.0, are the server-side alternative.)

`EVAL "return 'Hello, scripting!'" 0`: arguments are the script body, then the number of key-name arguments, then keys, then regular arguments.

Parameterise, never generate script text per call: `EVAL "return ARGV[1]" 0 Hello`. Generated variants fill the script cache and can exhaust memory.

Key rule: every key a script touches must be passed as a key argument, in standalone and cluster alike. Never access keys with computed names or names read from stored data. Key arguments arrive in the `KEYS` table and others in `ARGV`:
```
EVAL "return { KEYS[1], KEYS[2], ARGV[1], ARGV[2], ARGV[3] }" 2 key1 key2 arg1 arg2 arg3
```
Lua tables return as RESP2 arrays.

Calling commands: `server.call()` sends a runtime error straight to the client; `server.pcall()` returns it to the script to handle. Example: `EVAL "return server.call('SET', KEYS[1], ARGV[1])" 1 foo bar` gives `OK`.

Replication: the write commands a script issued are wrapped in `MULTI`/`EXEC` and sent to replicas and the AOF (effects replication). Verbatim script replication was removed.

## Checked
2026-11-03. Confirmed against the Valkey Scripting with Lua page (valkey.io/topics/eval-intro/): Lua 5.1, atomic blocking execution, the benefits list, eval scripts being client-side and not persisted, the `EVAL` argument layout, parameterisation and script-cache exhaustion, the KEYS/ARGV rule with the two-key example, RESP2 array replies, `server.call` versus `server.pcall`, and effects replication in MULTI/EXEC (verbatim replication removed in 7.0). The page carries an under-review notice. Nothing removed.
Method: documentation only; no commands were run.
