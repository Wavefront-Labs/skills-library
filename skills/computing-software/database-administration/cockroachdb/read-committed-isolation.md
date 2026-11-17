---
id: computing-software.database-administration.cockroachdb.read-committed-isolation
name: read-committed-isolation
category: computing-software
field: database-administration
product: cockroachdb
tags: [read-committed, isolation-levels, concurrency-anomalies, locking-reads, serializable]
level: practitioner
status: docs-checked
description: "Enable and use READ COMMITTED in CockroachDB: cluster setting, session, database and role defaults, behaviour differences, and anomalies to guard against."
sources:
  - https://www.cockroachlabs.com/docs/stable/read-committed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide whether to run `READ COMMITTED` and configure it safely. The default isolation is `SERIALIZABLE`; Cockroach Labs advises not switching a workload that already runs well, and suggests `READ COMMITTED` for high-concurrency workloads that tolerate anomalies or for migrations from apps built on it.

Enable: cluster setting `sql.txn.read_committed_isolation.enabled` is `true` by default. If it is `false`, `READ COMMITTED` transactions silently run as `SERIALIZABLE`; the DB Console SQL dashboard has an "Upgrades of SQL Transaction Isolation Level" graph to check.

Set the default:
```sql
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET default_transaction_isolation = 'read committed';
ALTER DATABASE db SET default_transaction_isolation = 'read committed';
ALTER ROLE foo SET default_transaction_isolation = 'read committed';
```
Per transaction: `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;` or `SET transaction_isolation = 'read committed';` as the first statement. Inspect with `SHOW default_transaction_isolation;` and `SHOW transaction_isolation;`.

Behaviour: statements see data committed before each statement began (not the transaction), concurrent writes interleave without aborts, and a write never blocks a non-locking read. This permits non-repeatable reads, phantom reads, lost updates and write skew. Mitigate with locking reads (`SELECT ... FOR UPDATE`). CockroachDB's version also prevents anomalies within a single statement, which is stronger than PostgreSQL's.

## Checked

2026-11-03. Confirmed against the Read Committed page: default isolation, `sql.txn.read_committed_isolation.enabled`, the upgrade graph, default and per-transaction syntax, anomalies and locking-read mitigation. Removed: invented verification step.
Method: documentation only; no commands were run.
