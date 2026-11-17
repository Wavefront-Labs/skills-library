---
id: computing-software.database-administration.valkey.script-cache-evalsha
name: script-cache-evalsha
category: computing-software
field: database-administration
product: valkey
tags: [script-cache, evalsha, script-load, noscript, script-kill, script-flush, sha1]
level: practitioner
status: docs-checked
description: "Valkey script cache: SCRIPT LOAD, EVALSHA, NOSCRIPT handling, cache volatility, SCRIPT FLUSH/EXISTS/SHOW/KILL, and EVALSHA inside pipelines."
sources:
  - https://valkey.io/topics/eval-intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every script run with `EVAL` is cached, keyed by its SHA1 digest. `INFO` shows `used_memory_scripts_eval` and `number_of_cached_scripts`, which grow with each distinct script. `SCRIPT LOAD "return 'x'"` compiles and caches without executing and returns the digest; run it with `EVALSHA <sha1> 0`.

The cache is always volatile and never persisted: it can vanish on restart, on failover when a replica takes over, or through `SCRIPT FLUSH`. Applications should call `EVALSHA` and, on `NOSCRIPT No matching script`, issue `SCRIPT LOAD` then retry; most clients do this automatically.

Pipelines: other clients commands can interleave, and a `NOSCRIPT` error from a pipelined `EVALSHA` cannot be handled mid-pipeline, so clients should fall back to plain parameterised `EVAL` there. Within one connection, scripts persist unless an admin flushes them or the server restarts (check `run_id` in `INFO` to detect a restart).

`SCRIPT` subcommands:
- `FLUSH`: only way to empty the cache; useful when an instance is reassigned or for testing client libraries.
- `EXISTS sha1 ...`: array of 1/0.
- `LOAD script`: guarantees `EVALSHA` will not fail, e.g. inside a pipeline or `MULTI`/`EXEC`.
- `SHOW`: returns the cached source.
- `KILL`: the only way to interrupt a slow script short of shutdown; slow means past the maximum execution time, and it works only if the script has not yet modified data (preserving atomicity).
- `DEBUG`: controls the built-in Lua debugger.

Well-behaved apps keep scripts cached indefinitely; hundreds of scripts use little memory.

## Checked
2026-11-03. Confirmed against the Valkey Scripting with Lua page (valkey.io/topics/eval-intro/): SHA1-keyed cache, `used_memory_scripts_eval` and `number_of_cached_scripts`, `SCRIPT LOAD` and `EVALSHA`, cache volatility on restart, failover and `SCRIPT FLUSH`, the `NOSCRIPT No matching script` flow, EVALSHA inside pipelines, the `run_id` restart check, and all `SCRIPT` subcommands including `KILL` limits. The page carries an under-review notice. Nothing removed.
Method: documentation only; no commands were run.
