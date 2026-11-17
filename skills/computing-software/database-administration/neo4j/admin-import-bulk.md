---
id: computing-software.database-administration.neo4j.admin-import-bulk
name: admin-import-bulk
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-admin-import, bulk-import, incremental-import, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Offline bulk load"
sources:
  - https://neo4j.com/docs/operations-manual/current/import/full-import/
  - https://neo4j.com/docs/operations-manual/current/import/incremental-import/
  - https://neo4j.com/docs/operations-manual/current/import/header-format/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# neo4j-admin database import

Goal: load billions of records fast.
- `neo4j-admin database import full --nodes=Person=people.csv --relationships=KNOWS=knows.csv mydb` (the `--nodes` and `--relationships` options are documented on the full import page).
- If the database does not exist before importing, create it afterwards with `CREATE DATABASE`.
- `neo4j-admin database import incremental` exists and is an Enterprise Edition feature.
- Headers declare ids, types and labels; see the header format page.
- Pre-sort and clean data; fix errors in the import report.
Verify: `CALL db.stats.retrieve('GRAPH COUNTS')` matches inputs.

## Checked

2026-11-02. Confirmed in the full import, incremental import and procedures pages (`CREATE DATABASE` afterwards, `import [full|incremental]`, `db.stats.retrieve` section `GRAPH COUNTS`). Removed: the claim that full mode requires a database that must not exist (the page only says to create it afterwards).
Method: documentation only; no commands were run.
