---
id: computing-software.database-administration.neo4j.call-in-transactions
name: call-in-transactions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, in-transactions, batch-commit, on-error, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Batching writes"
sources:
  - https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CALL IN TRANSACTIONS

Goal: avoid huge transactions.
- `LOAD CSV ... CALL { ... } IN TRANSACTIONS OF 10000 ROWS`; the default batch size is 1000 rows.
- Only allowed in implicit (auto-commit) transactions; in Neo4j Browser prepend `:auto`.
- `ON ERROR CONTINUE | BREAK | FAIL | RETRY` controls failure handling; `FAIL` is the default.
- Inner transactions that committed stay committed if a later one fails.
Verify: after a forced failure, earlier batches are still committed.

## Checked

2026-11-02. Confirmed: batch size and default, implicit-transaction rule, `:auto`, the four `ON ERROR` modes and default, committed inner transactions kept (subqueries-in-transactions). Removed: the 'confirm version' hedge and the 'heap stays flat' claim.
Method: documentation only; no commands were run.
