---
id: computing-software.database-administration.neo4j.cdc-enable-and-consume
name: cdc-enable-and-consume
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, cdc-enable, db-cdc-query, change-identifier, neo4j-cdc, change-streams, kafka-connector, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Change feeds"
sources: ["https://neo4j.com/docs/cdc/current/get-started/self-managed/", "https://neo4j.com/docs/cdc/current/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling and consuming CDC

Goal: stream graph changes.
- CDC is an Enterprise Edition and Aura feature, introduced in 5.13.
- Enable on a new database: `CREATE DATABASE <dbName> IF NOT EXISTS OPTIONS {txLogEnrichment: "FULL"}`; on an existing one: `ALTER DATABASE <dbName> SET OPTION txLogEnrichment "DIFF"`. The values are `FULL` and `DIFF`.
- Consume with `db.cdc.query`, which needs admin privileges (or execute plus boosted execute privileges for a regular user); `db.cdc.current` and `db.cdc.earliest` need only regular execute privileges.
- Data written by `neo4j-admin database import` (full or incremental) or `load` bypasses the transaction layer and is not captured.
- CDC writes more into transaction logs, so logs rotate and prune more often.
Verify: an update after enabling produces a change event from `db.cdc.query`.

## Checked

2026-11-02. Confirmed in the CDC self-managed page and the CDC landing page. Removed: the `db.cdc.query(from, selectors)` signature and the 'store the last change identifier' advice (argument list not read).
Method: documentation only; no commands were run.
