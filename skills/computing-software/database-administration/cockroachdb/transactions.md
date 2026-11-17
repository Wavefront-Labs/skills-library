---
id: computing-software.database-administration.cockroachdb.transactions
name: transactions
category: computing-software
field: database-administration
product: cockroachdb
tags: [transactions, serializable, retries, savepoints, transaction-priority]
level: practitioner
status: docs-checked
description: "Use CockroachDB transactions correctly: BEGIN/COMMIT, error classes 40001 and 40003, automatic versus client retries, savepoints and priorities."
sources:
  - https://www.cockroachlabs.com/docs/stable/transactions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write and troubleshoot multi-statement transactions that survive contention.

Statements: `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `RELEASE SAVEPOINT`, `ROLLBACK TO SAVEPOINT` and `SET TRANSACTION`.

Error classes your client must distinguish:
- Code `40001` ("restart transaction"): the transaction could not be placed in a serializable order. Retry the whole transaction.
- Code `40003`: ambiguous result; you cannot assume it committed or failed; how to resolve it depends on how you want to handle the ambiguity (see the common errors page).
- Other SQL errors (for example `23505` from a UNIQUE violation): a statement failed; issue `COMMIT` or `ROLLBACK`.

Retries:
- Automatic: single statements (implicit transactions) and transactions sent as one batch are retried by the server while the results sent to the client are under 16KiB by default. `INSERT`/`UPDATE`/`DELETE` without `RETURNING` always fit. The `enable_implicit_transaction_for_batch_statements` session variable defaults to `true`.
- Conditional logic that depends on earlier results cannot be batched, so the client needs its own retry loop with exponential backoff (or the savepoint protocol `SAVEPOINT cockroach_restart` ... `RELEASE SAVEPOINT cockroach_restart`).

Nested transactions use savepoints; `ROLLBACK TO SAVEPOINT` discards only the inner work.

Priority: `BEGIN PRIORITY LOW|NORMAL|HIGH`, `SET TRANSACTION PRIORITY ...`, or the `default_transaction_priority` session variable; `SHOW transaction_priority` is read-only.

## Checked

2026-11-03. Confirmed against the transactions page: statements, error classes `40001`, `40003` and `23505`, the 16KiB automatic-retry buffer, `enable_implicit_transaction_for_batch_statements`, exponential-backoff retry loop, `SAVEPOINT cockroach_restart`, nested transactions, priority syntax and `transaction_priority`. Removed: the invented two-session verification step and the generic `SHOW` claim.
Method: documentation only; no commands were run.
