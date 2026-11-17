---
id: computing-software.database-administration.neo4j.multi-database-management
name: multi-database-management
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, create-database, start-stop-database, show-databases, composite-database, database-state, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Enterprise multi-db"
sources:
  - https://neo4j.com/docs/operations-manual/current/database-administration/
  - https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/create-databases/
  - https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/start-stop-databases/
  - https://neo4j.com/docs/operations-manual/current/database-administration/aliases/manage-aliases-standard-databases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple databases

Goal: manage databases.
- `CREATE DATABASE actors IF NOT EXISTS`; `STOP DATABASE sales`; `START DATABASE sales`; `SHOW DATABASES`.
- Community Edition installations can have exactly one standard database, besides `system`.
- Aliases: `CREATE ALIAS yard FOR DATABASE garden`.
Verify: `SHOW DATABASES` shows the database online.

## Checked

2026-11-02. Confirmed: create/start/stop/show commands, Community Edition limit, alias syntax (database-administration index, create-databases, start-stop-databases, aliases).
Method: documentation only; no commands were run.
