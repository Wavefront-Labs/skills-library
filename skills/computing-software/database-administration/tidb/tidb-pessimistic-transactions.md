---
id: computing-software.database-administration.tidb.tidb-pessimistic-transactions
name: tidb-pessimistic-transactions
category: computing-software
field: database-administration
product: tidb
tags: [tidb, pessimistic-transaction, tidb-txn-mode, select-for-update, deadlock, lock-wait-timeout, nowait, snapshot-read, current-read]
level: practitioner
status: docs-checked
description: "Use TiDB pessimistic transactions: switching modes, snapshot versus current reads, lock behaviour, deadlock and timeout error codes, NOWAIT and MySQL differences."
sources: ["https://docs.pingcap.com/tidb/stable/pessimistic-transaction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb pessimistic transactions

Pessimistic mode (since v3.0) makes TiDB behave like traditional databases. Clusters newly created on v3.0.8 or later default to it; upgraded clusters keep their earlier mode.

Switching: `SET GLOBAL tidb_txn_mode = 'pessimistic';` affects explicit (non-autocommit) transactions in newly created sessions. `BEGIN PESSIMISTIC;` or `BEGIN /*T! PESSIMISTIC */;` (and `BEGIN OPTIMISTIC;`) override the variable. Both modes can coexist in a cluster.

Behaviour:
- Snapshot read: unlocked, reads the version committed before the transaction started (plain `SELECT`).
- Current read: locked, reads the latest committed version (`UPDATE`, `DELETE`, `INSERT`, `SELECT FOR UPDATE`).
- `UPDATE/DELETE/INSERT` lock modified rows. `SELECT FOR UPDATE` locks the latest committed version.
- Locks release on commit or rollback. Writers wait; plain readers are not blocked because of MVCC.
- Deadlocks are detected automatically and one transaction is terminated with MySQL error 1213.
- Lock waits time out after `innodb_lock_wait_timeout` seconds (default 50) with error 1205.
- `FOR UPDATE NOWAIT` does not wait and returns error 3572.
- `Point Get` and `Batch Point Get` lock the key even when no row is found (under Repeatable Read).
- `FOR UPDATE OF tables` locks only rows from the named tables in a join.
- `tidb_constraint_check_in_place_pessimistic` controls whether unique-constraint checks lock in place.

Difference from InnoDB: a range `SELECT ... FOR UPDATE` does not block concurrent inserts inside the range (no gap locks), so an insert of id 6 into a locked range 1..10 succeeds in TiDB but blocks in MySQL.

## Checked

2026-11-04. Confirmed against the TiDB Pessimistic Transaction Mode page: v3.0 and v3.0.8 defaults, mode switching, snapshot and current reads, error codes 1213, 1205 and 3572, lock-wait default, Point Get locking under Repeatable Read, FOR UPDATE OF, gap-lock difference.
Method: documentation only; no commands were run.
