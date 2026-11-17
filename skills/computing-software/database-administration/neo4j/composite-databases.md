---
id: computing-software.database-administration.neo4j.composite-databases
name: composite-databases
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, composite-database, fabric, federated-queries, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Federation"
sources:
  - https://neo4j.com/docs/operations-manual/current/scalability/composite-databases/concepts/
  - https://neo4j.com/docs/operations-manual/current/scalability/composite-databases/querying-composite-databases/
  - https://neo4j.com/docs/operations-manual/current/database-administration/aliases/manage-aliases-composite-databases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite databases

Goal: query multiple databases together.
- `CREATE COMPOSITE DATABASE name [IF NOT EXISTS]`; constituents are added as aliases named inside it, for example ``CREATE ALIAS `library.sci-fi` FOR DATABASE `sci-fi-books` ``.
- Queries direct parts to constituent graphs with `USE <composite>.<alias>`; a query may contain several `USE` clauses.
- A transaction may read from multiple graphs, or read from multiple graphs and write to a single graph.
- Used for data federation and for sharding data that shares one model.
Verify: a federated query returns data from both constituents.

## Checked

2026-11-02. Confirmed: create syntax, alias naming, `USE`, read/write limits, federation and sharding uses (composite-databases pages, manage-aliases-composite-databases, syntax). Removed: 'limited writes (confirm)' in favour of the exact rule.
Method: documentation only; no commands were run.
