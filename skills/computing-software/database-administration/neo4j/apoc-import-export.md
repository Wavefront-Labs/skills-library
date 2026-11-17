---
id: computing-software.database-administration.neo4j.apoc-import-export
name: apoc-import-export
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, apoc-import-json, apoc-export-csv, apoc-load-jdbc, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Data movement"
sources: ["https://neo4j.com/docs/apoc/current/export/csv/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APOC import/export

Goal: move data with APOC.
- Export procedures: `apoc.export.csv.all(file, config)` (whole database), `apoc.export.csv.data`, `apoc.export.csv.graph` and `apoc.export.csv.query`.
- File export must be enabled with `apoc.export.file.enabled=true` in the configuration.
- `apoc.load.json` and `apoc.load.jdbc` are the load procedures for JSON and relational sources.
Verify: an exported file re-imports to an equal graph.

## Checked

2026-11-02. Confirmed in the APOC CSV export page and the APOC overview text. Removed: secrets-management advice (not on those pages).
Method: documentation only; no commands were run.
