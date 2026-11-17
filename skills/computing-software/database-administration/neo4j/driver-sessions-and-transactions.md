---
id: computing-software.database-administration.neo4j.driver-sessions-and-transactions
name: driver-sessions-and-transactions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, execute-query, transaction-functions, managed-transactions, neo4j-driver, bolt-protocol, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Using drivers"
sources: ["https://neo4j.com/docs/python-manual/current/transactions/", "https://neo4j.com/docs/python-manual/current/query-simple/", "https://neo4j.com/docs/python-manual/current/performance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions, transactions and retries

Goal: write resilient clients (Python driver shown).
- `session.execute_read()` and `session.execute_write()` run managed transactions; the driver retries transient failures until the configured maximum retry time, so transaction functions must be idempotent (do not edit or rely on globals).
- `driver.execute_query()` is the simple entry point for single queries.
- Name the database in `driver.session(database="<name>")` or the `database_` parameter of `execute_query`, otherwise the driver makes an extra request to find the default database.
Verify: a transient failure causes a retry, not a visible error.

## Checked

2026-11-02. Confirmed in the Python driver transactions, simple queries and performance pages. Removed: 'one driver per application' and 'short-lived sessions' (not on those pages), and the kill-a-cluster-member test.
Method: documentation only; no commands were run.
