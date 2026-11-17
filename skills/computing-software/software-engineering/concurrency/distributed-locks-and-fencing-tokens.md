---
id: computing-software.software-engineering.concurrency.distributed-locks-and-fencing-tokens
name: distributed-locks-and-fencing-tokens
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, distributed-systems, distributed-locks, fencing-tokens, leases, redlock, etcd]
level: sme
status: draft
description: "Use distributed locks correctly: leases with expiry, fencing tokens checked by the resource, why Redis Redlock is unsafe for correctness, and etcd/ZooKeeper/database alternatives."
sources: ["https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html", "https://redis.io/docs/latest/develop/use/patterns/distributed-locks/", "https://etcd.io/docs/v3.5/dev-guide/api_concurrency_reference_v3/", "https://www.postgresql.org/docs/current/explicit-locking.html#ADVISORY-LOCKS"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distributed locks and fencing tokens

## First ask: efficiency or correctness?
- **Efficiency** (avoid doing the same work twice; occasional duplicates are OK): a simple Redis
  `SET key token NX PX 30000` with token-checked release is fine.
- **Correctness** (two holders would corrupt data): you need a lock service with consensus *and*
  fencing; timing-based locks alone are unsafe.

## Why leases are not enough
Every distributed lock needs an expiry (holders crash). But a holder can pause past expiry (GC
pause, VM migration, network delay) and keep acting while another client holds the lock.
Kleppmann's example: client 1 pauses, lease expires, client 2 acquires and writes, client 1 wakes
and writes stale data.

## Fencing tokens
The lock service returns a **monotonically increasing token** with each grant. Every write to the
protected resource includes the token; the **resource rejects tokens lower than the highest seen**.
```sql
UPDATE jobs SET state = 'done', fence = :token
WHERE id = :id AND fence < :token;      -- 0 rows -> we were fenced off; abort
```
Sources of tokens: etcd revision (`mod_revision`/lease key create revision), ZooKeeper `zxid` or
sequential znode number, a database sequence incremented on acquisition.

## Tools
- **etcd** (`concurrency.NewMutex` / `etcdctl lock`) and **ZooKeeper** (Curator `InterProcessMutex`):
  consensus-based, give tokens. Keep sessions alive; handle session loss as "lost the lock".
- **Database**: Postgres advisory locks (`pg_try_advisory_lock(key)`, session- or transaction-scoped),
  `SELECT ... FOR UPDATE SKIP LOCKED` for job claiming; correctness tied to the DB connection.
- **Redis**: single-instance `SET NX PX` with release via Lua compare-and-delete. **Redlock**
  (multi-instance) relies on bounded clock drift and pauses; Kleppmann argues it's unsafe for
  correctness. Use for efficiency only.

## Release safely
Only delete if the value is still your token (Lua: `if redis.call("get",KEYS[1]) == ARGV[1] then
return redis.call("del",KEYS[1]) end`). Renew leases well before expiry; stop work if renewal fails.

## Often better
Avoid the lock: idempotent operations, single-writer partitioning (Kafka partition ownership),
optimistic concurrency (version columns, compare-and-swap).
