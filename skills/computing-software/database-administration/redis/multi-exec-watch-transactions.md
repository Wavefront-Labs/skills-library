---
id: computing-software.database-administration.redis.multi-exec-watch-transactions
name: multi-exec-watch-transactions
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, transactions, multi, exec, watch, optimistic-locking, lua, atomicity]
level: practitioner
status: docs-checked
description: "Use Redis MULTI/EXEC for atomic batches and WATCH for optimistic locking, understand the no-rollback error model, and know when a Lua script is the better tool."
sources:
  - https://redis.io/docs/latest/develop/using-commands/transactions/
  - https://redis.io/docs/latest/develop/using-commands/multi-key-operations/
  - https://redis.io/docs/latest/develop/clients/redis-py/transpipe/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MULTI / EXEC / WATCH transactions

**Goal:** apply several commands as one atomic unit, and do read-modify-write without lost updates.

## MULTI/EXEC
```text
MULTI
DECRBY stock:sku9 1
LPUSH orders:pending "o-77"
EXEC          # both run back-to-back, nothing interleaves
DISCARD       # instead of EXEC: drop the queue
```
Commands are queued (`QUEUED`) and executed at EXEC. A request from another client is never served in the middle
of a transaction. If the connection drops before EXEC, none of the commands run.

## Errors: no rollback
- Error while queuing (wrong arity or command name, or a critical condition such as OOM with `maxmemory`): the
  server refuses to run the transaction and `EXEC` returns an error, discarding it.
- Error after EXEC (for example a list command on a string key, `WRONGTYPE`): that command's reply is an error,
  **the other commands still execute**. Redis does not support rollbacks, for simplicity and performance;
  validate before.

## Optimistic locking with WATCH
```text
WATCH balance:alice
GET balance:alice           # read, decide in the client
MULTI
DECRBY balance:alice 30
INCRBY balance:bob 30
EXEC                        # returns a null reply if a watched key changed since WATCH -> retry the whole loop
```
In code: loop { WATCH; read; compute; MULTI; writes; EXEC } until EXEC is not null, with a retry cap. In redis-py, a
pipeline is a transaction by default (`transaction=True`); use `pipe.watch(...)` then `pipe.multi()`, or the
`r.transaction(func, *watched_keys)` helper, which retries on `WatchError`.

`WATCH` covers changes by any client and by Redis itself (expiration, eviction); before 6.0.9 an expired key did not
abort the transaction. All keys are unwatched when `EXEC` is called, whether it aborted or not, and when the connection
closes; `UNWATCH` clears them manually. Commands queued inside the transaction do not trigger the watch condition.
Redis 8.4+ adds single-command compare-and-set (`SET ... IFEQ`) and compare-and-delete (`DELEX`) for string keys,
which are simpler than WATCH for those cases.

## Transactions vs Lua/Functions
| | MULTI/EXEC | Script / Function |
|---|---|---|
| Conditional logic on read values | Only via WATCH retry loop | Inside the script |
| Round trips | WATCH + reads + EXEC | One |
| Contention | Retries under contention | No retries |
The documentation notes that everything you can do with a transaction you can do with a script, usually simpler and
faster. Use scripts when logic depends on reads under contention; MULTI for simple batched atomic writes.

## Cluster
In a cluster, all keys in a `MULTI/EXEC` transaction must be in the same hash slot (use hash tags).

## Verify
Two clients run the WATCH loop on the same key concurrently 1000 times each; final value equals the expected total (no lost updates).

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): Transactions page, multi-key operations
page, redis-py pipelines and transactions page. Confirmed: isolation and all-or-nothing on disconnect, the two error
classes and their handling, no rollbacks, WATCH semantics (EXEC unwatches, 6.0.9 expiry change, queued commands do not
trigger), redis-py defaults and `transaction()` helper, 8.4 compare-and-set, single-slot rule for transactions in a
cluster. Removed: the literal `EXECABORT` error name (the page says only that EXEC returns an error), and "WATCH is
cleared after DISCARD" (the page lists EXEC, UNWATCH and connection close).
Method: documentation only; no commands were run.
