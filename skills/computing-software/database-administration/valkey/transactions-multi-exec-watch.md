---
id: computing-software.database-administration.valkey.transactions-multi-exec-watch
name: transactions-multi-exec-watch
category: computing-software
field: database-administration
product: valkey
tags: [transactions, multi, exec, discard, watch, unwatch, execabort, optimistic-locking, cas]
level: practitioner
status: docs-checked
description: "Valkey transactions: MULTI, EXEC, DISCARD, WATCH optimistic locking, error behaviour (EXECABORT, no rollback), MOVED/REDIRECT in EXEC."
sources:
  - https://valkey.io/topics/transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MULTI` starts a transaction (reply `OK`); later commands reply `QUEUED`; `EXEC` runs them all and returns an array of replies in order; `DISCARD` flushes the queue and leaves the transaction. Guarantees: commands run sequentially with no other client served in the middle, and either all run (after `EXEC`) or none (connection lost before `EXEC`). With AOF a transaction is written in a single `write(2)`; after a hard crash a partial transaction is detected at restart, startup fails, and `valkey-check-aof` removes it.

Errors: a command that cannot be queued (wrong arity or name, or out-of-memory with `maxmemory`) makes `EXEC` return `EXECABORT` and discard everything. A command that fails after `EXEC` (e.g. `LPOP` on a string, `WRONGTYPE`) is just an error entry in the reply array; all other commands still run. There is no rollback, to keep Valkey simple and fast.

Cluster and failover: at `EXEC`, if a slot migration (cluster) or failover (standalone) happened since queuing, the reply is `-MOVED` or `-REDIRECT` without running anything. A command touching data not on this node gets `-MOVED`/`-REDIRECT` immediately and `EXEC` returns `EXECABORT`.

Optimistic locking: `WATCH key ...` makes `EXEC` conditional. If any watched key changed (by a client, or by expiry or eviction) after `WATCH`, `EXEC` returns a Null reply and nothing runs; retry. Commands queued inside the transaction do not trigger it. `EXEC` or disconnect unwatches all keys; `UNWATCH` clears manually.

Pattern: `WATCH zset`, `ZRANGE zset 0 0`, `MULTI`, `ZREM zset element`, `EXEC`, repeating on Null, emulates `ZPOPMIN`.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/transactions/ (page text read in full): MULTI/QUEUED/EXEC/DISCARD, isolation and all-or-nothing guarantees, single write(2) with AOF and valkey-check-aof, EXECABORT cases, WRONGTYPE after EXEC, no rollback, -MOVED/-REDIRECT behaviour, WATCH semantics (Null reply, expiry/eviction, UNWATCH), ZPOPMIN pattern.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
