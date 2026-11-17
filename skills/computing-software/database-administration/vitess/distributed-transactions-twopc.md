---
id: computing-software.database-administration.vitess.distributed-transactions-twopc
name: distributed-transactions-twopc
category: computing-software
field: database-administration
product: vitess
tags: [transactions, twopc, transaction-mode, distributed-transaction, semi-sync, dtid]
level: advanced
status: docs-checked
description: "Choose single, multi or twopc transaction mode in Vitess, enable TwoPC on VTGate and VTTablet, and monitor or repair unresolved transactions."
sources:
  - https://vitess.io/docs/25.0/reference/features/distributed-transaction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess has three transaction modes. `single` limits transactions to one shard (full ACID). `multi` (the default) may span shards with best-effort commits and no atomicity. `twopc` gives atomic commits across shards but not isolation: cross-shard reads can see fractured, partially committed state, and commit latency rises, so design the VSchema to minimise cross-shard writes.

Configuration:
- VTGate default: `transaction_mode=multi|single|twopc`; per session `SET transaction_mode='twopc';`.
- VTTablet: `--twopc-enable` and `--twopc-abandon-age=300` (seconds before a transaction is treated as abandoned; recommended 5-10 minutes). The transaction watcher uses it to signal VTGate to resolve.
- MySQL: semi-sync replication is required (TwoPC rolls back without it) and `wait_timeout` must not be short (default 28800) so prepared transactions are not dropped.

Monitoring: after a commit failure run `show warnings` to get the DTID, then `show transaction status for <dtid>;` which returns id, state (for example PREPARE), record_time and participants. VTGate metrics: CommitModeTimings, CommitUnresolved, QueriesRouted (PlanType Commit). VTTablet: QueryTimings (CreateTransaction, Prepare, StartCommit, SetRollback, CommitPrepared, RollbackPrepared, Resolve) and Unresolved.

Critical counters that should stay zero: InternalErrors.TwopcOpen, TwopcCommit, TwopcPrepareRedo, TwopcResurrection. Alertable: RedoWatcherFail, TransactionWatcherFail.

Repair: find the DTID in VTGate/VTTablet logs, view in-flight transactions per keyspace in VTAdmin, repair manually, then force `Conclude` to clear it from the unresolved list.

## Checked

2026-11-08. Read in full: Distributed Transactions page (vitess.io docs 25.0, via the website repo markdown). Confirmed: the three modes and the isolation caveat, transaction_mode settings, VTTablet flags and abandon age, semi-sync and wait_timeout prerequisites, SHOW TRANSACTION STATUS, metric names and the repair flow. Nothing removed.

Method: documentation only; no commands were run.
