---
id: computing-software.database-administration.neo4j.query-logging
name: query-logging
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, query-log, log-queries-threshold, show-transactions, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Finding slow queries"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
  - https://neo4j.com/docs/operations-manual/current/monitoring/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query logging and slow queries

Goal: identify slow work.
- `db.logs.query.enabled` takes OFF, INFO (log queries slower than `db.logs.query.threshold`) or VERBOSE (log start and end of every query).
- `SHOW TRANSACTIONS` lists running transactions and `TERMINATE TRANSACTION '<id>'` ends them.
- `db.logs.query.parameter_logging_enabled` logs parameters, so treat the log as sensitive.
Verify: slow queries appear in query.log.

## Checked

2026-11-02. Confirmed in the configuration settings reference (`db.logs.query.enabled` modes, `db.logs.query.threshold`, `db.logs.query.parameter_logging_enabled`) and the transactions pages (`TERMINATE TRANSACTION 'neo4j-transaction-1'`). Removed: the 1s example threshold.
Method: documentation only; no commands were run.
