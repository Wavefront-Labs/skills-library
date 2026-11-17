---
id: computing-software.database-administration.neo4j.load-csv-import
name: load-csv-import
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, load-csv, periodic-commit, csv-import, neo4j-admin-import, import-tools, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Online import"
sources:
  - https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LOAD CSV

Goal: import CSV with Cypher.
- Create constraints first, then `LOAD CSV WITH HEADERS FROM 'file:///x.csv' AS row MERGE (...)`.
- `file:///` paths resolve relative to the Neo4j import directory (`server.directories.import`).
- Batch with `CALL { ... } IN TRANSACTIONS`.
Verify: node and relationship counts match source rows.

## Checked

2026-11-02. Confirmed in the LOAD CSV page and configuration settings reference (`server.directories.import`). Removed: the Eager-avoidance advice.
Method: documentation only; no commands were run.
