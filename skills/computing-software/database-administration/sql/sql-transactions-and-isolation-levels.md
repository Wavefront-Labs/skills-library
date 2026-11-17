---
id: computing-software.database-administration.sql.sql-transactions-and-isolation-levels
name: sql-transactions-and-isolation-levels
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-transactions, isolation-levels, acid, read-committed, serializable]
level: advanced
status: docs-checked
description: "Choose isolation levels in PostgreSQL and SQLite, knowing which anomalies each prevents, and retry on serialization failure."
sources: ["https://www.postgresql.org/docs/current/transaction-iso.html", "https://www.postgresql.org/docs/current/sql-set-transaction.html", "https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html", "https://www.postgresql.org/docs/current/errcodes-appendix.html", "https://www.sqlite.org/isolation.html", "https://www.sqlite.org/lang_transaction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions and isolation

- The SQL standard defines four levels in terms of phenomena: dirty read, nonrepeatable read, phantom read, and serialization anomaly (a committed group of transactions that matches no one-at-a-time order). Standard table: READ UNCOMMITTED allows dirty reads, nonrepeatable reads and phantoms; READ COMMITTED allows the last two; REPEATABLE READ allows phantoms; SERIALIZABLE allows none. Serialization anomalies are possible below SERIALIZABLE.
- PostgreSQL: the default is READ COMMITTED (each statement sees data committed before it began, so two successive SELECTs in one transaction can differ). READ UNCOMMITTED behaves as READ COMMITTED, so only three levels are really implemented. REPEATABLE READ does not allow phantom reads, which the standard permits as a stronger guarantee, but a serialization anomaly is still possible. SERIALIZABLE uses Serializable Snapshot Isolation and rolls back one of two transactions that have no consistent serial order.
- Both REPEATABLE READ and SERIALIZABLE can raise errors with SQLSTATE `40001` (serialization_failure). Retry the whole transaction, including the logic that chooses the SQL and values; PostgreSQL has no automatic retry. A retry may itself fail, so allow several attempts.
- Deadlocks have SQLSTATE `40P01` (deadlock_detected) and may also be worth retrying. Unique violations (`23505`) and exclusion violations (`23P01`) are sometimes retryable too, but may be persistent errors, so retry them with more care than `40001`.
- Set the level per transaction with `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;` or `SET TRANSACTION ISOLATION LEVEL ...` (it affects only the current transaction). `SET SESSION CHARACTERISTICS` or `default_transaction_isolation` set defaults.
- Sequence changes are visible immediately and are not rolled back when a transaction aborts.
- For serializable workloads PostgreSQL advises using a connection pool to limit active connections and removing explicit locks (`SELECT FOR UPDATE/SHARE`) that serializable protections make unnecessary.
- SQLite: transactions are SERIALIZABLE (writes are serialized, one writer at a time), except between shared-cache connections with `PRAGMA read_uncommitted` on. `BEGIN` is DEFERRED by default; `BEGIN IMMEDIATE` starts a write transaction at once and can fail with SQLITE_BUSY if another writer is active. In WAL mode (`PRAGMA journal_mode=WAL`) readers see a snapshot, and a read transaction that tries to write after another connection committed fails with SQLITE_BUSY_SNAPSHOT.
- There is no isolation between statements on the same SQLite connection.
- Keep transactions short; do not hold them open across user input or network calls.

## Checked

2026-11-08. Confirmed against the PostgreSQL Transaction Isolation, SET TRANSACTION, Serialization Failure Handling and Error Codes appendix pages and the SQLite Isolation and Transaction pages. Removed claims not covered by those pages: MySQL InnoDB gap locks and default, SQL Server defaults, DDL transactionality per engine, SAVEPOINT and autocommit behaviour, and the exact phrase "write skew" (the docs state that serialization anomalies remain possible at REPEATABLE READ). Description narrowed to the engines checked.

Method: documentation only; no commands were run.
