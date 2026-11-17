---
id: computing-software.database-administration.neo4j.transaction-timeouts-limits
name: transaction-timeouts-limits
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, transaction-timeout, max-concurrent-transactions, terminate-transaction, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Governance"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
  - https://neo4j.com/docs/operations-manual/current/monitoring/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction timeouts and limits

Goal: bound runaway queries.
- `db.transaction.timeout`, `db.transaction.concurrent.maximum`, `db.memory.transaction.max` (per transaction) and `dbms.memory.transaction.total.max` / `db.memory.transaction.total.max` (totals) are documented settings.
- `TERMINATE TRANSACTIONS` ends runaway transactions.
Verify: a deliberately slow query is terminated at the limit.

## Checked

2026-11-02. Confirmed in the configuration settings reference (all five setting names) and the Cypher manual transactions pages (`TERMINATE TRANSACTIONS`). Removed: the driver per-transaction timeout claim.
Method: documentation only; no commands were run.
