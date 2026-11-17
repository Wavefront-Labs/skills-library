---
id: computing-software.database-administration.postgresql.lock-management-settings
name: lock-management-settings
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgresql-conf, max-locks-per-transaction, deadlock-timeout, out-of-shared-memory, lock-table]
level: practitioner
status: verified
description: "Fix 'out of shared memory, increase max_locks_per_transaction' on partitioned or many-table workloads and tune deadlock_timeout with log_lock_waits."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-locks.html
  - https://www.postgresql.org/docs/current/view-pg-locks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock management settings

## max_locks_per_transaction
The shared lock table has room for roughly
`max_locks_per_transaction * (max_connections + max_prepared_transactions)` object locks.
It is a pool, not a per-transaction cap, but one session touching thousands of relations
exhausts it:
```
ERROR:  out of shared memory
HINT:  You might need to increase "max_locks_per_transaction".
```
Typical triggers: queries over a partitioned table with thousands of partitions (every
partition and its indexes is locked when pruning cannot happen at plan time), `pg_dump` of a
database with tens of thousands of tables, `DROP SCHEMA ... CASCADE`, big migrations in one
transaction.

The nominal formula is only a guide: with `max_locks_per_transaction = 10` and `max_connections = 20` (nominal 200 locks) a single transaction creating partitions failed at the 1133rd partition, because the lock table has some slack. Set it from observed need, not the formula.
```sql
SHOW max_locks_per_transaction;                 -- default 64
ALTER SYSTEM SET max_locks_per_transaction = 256;  -- restart required
```
Each slot costs a few hundred bytes of shared memory; 256-1024 is fine on modern hosts.
**Standbys must have a value >= the primary.** A standby started with a lower value refuses to start recovery: `FATAL: recovery aborted because of insufficient parameter settings`, `DETAIL: max_locks_per_transaction = 10 is a lower setting than on the primary server, where its value was 64.` If the primary is raised while a standby is running, the standby logs `WARNING: hot standby is not possible because of insufficient parameter settings` and `recovery has paused` (it stays up with replay paused and shuts down if unpaused); restart it with the new value. Raise standbys first.

Reduce demand too: make partition pruning happen (use literal or parameter keys on the
partition column), keep partition counts in the hundreds, split huge migrations, and for
`pg_dump` raise the setting rather than dumping with `--jobs` across many relations at once.

## deadlock_timeout (default 1s)
How long a waiter sleeps before running the deadlock detector. Also the threshold for
`log_lock_waits`:
```sql
ALTER SYSTEM SET log_lock_waits = on;   -- logs "still waiting for ShareLock ... after 1000.123 ms"
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();
```
- Lower it (200ms) only if you want lock-wait logging sooner and deadlocks are rare; the
  detector is not free on busy systems.
- Raise it (2-5s) on very high-concurrency systems with short waits to cut detector overhead.

## Related limits
- `max_pred_locks_per_transaction` / `max_pred_locks_per_relation`: same "out of shared
  memory" message but for SERIALIZABLE predicate locks.
- `lock_timeout`: per-statement cap on lock waiting; set it for DDL in migrations.

## Verify
```sql
SELECT count(*) FROM pg_locks;                              -- current lock table usage
SELECT pid, count(*) FROM pg_locks GROUP BY pid ORDER BY 2 DESC LIMIT 5;
```
Re-run the failing workload; the error disappears and log lines show waits above
`deadlock_timeout` only.

## Checked
Run on PostgreSQL 17.6 (Windows build, two to eight real sessions via psycopg 3.3) on Windows with throwaway clusters: `ERROR: out of shared memory` with `HINT: You might need to increase "max_locks_per_transaction".` from a plain `SELECT count(*)` over a 3000-partition table, from `CREATE TABLE ... PARTITION OF` in one transaction, and from `pg_dump -s` (its `LOCK TABLE` list); queries pruned by a literal or a prepared-statement parameter did not fail; the same full scan still failed at 64; the two standby behaviours above (start refused; running standby pauses replay); `log_lock_waits` log lines after `deadlock_timeout` (1 s); `deadlock_timeout` is reloadable with `pg_reload_conf()` (documented, the lock waits were logged at the default) and `max_locks_per_transaction` needed a restart. Not run: `max_pred_locks_per_transaction` and SERIALIZABLE predicate locks, raising `deadlock_timeout` effects, the shared memory cost per slot, Linux.
