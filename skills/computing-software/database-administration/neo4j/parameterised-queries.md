---
id: computing-software.database-administration.neo4j.parameterised-queries
name: parameterised-queries
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, parameters, query-plan-cache, string-concatenation, query-parameters, cypher-injection, plan-cache, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Always parameterise"
sources:
  - https://neo4j.com/docs/cypher-manual/current/syntax/parameters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameterised queries

Goal: write injection-safe, cache-friendly queries.
- Pass `$name` instead of building strings; the docs say parameters make caching of execution plans easier.
- Parameters cannot be used for property keys, relationship types or node labels written statically (`MATCH (n:$param)` is invalid); dynamic labels and types are a separate syntax, see `MATCH` using dynamic node labels and relationship types.
- `:param name => 'Joe'` sets a parameter in Cypher Shell and Neo4j Browser.
Verify: the same query text is reused for different values.

## Checked

2026-11-02. Confirmed: parameter uses and limits, plan-caching remark, `:param` (syntax/parameters). Fixed: the draft said labels and types can never be parameters; the page now documents dynamic labels and types. Removed: the query-log verification claim.
Method: documentation only; no commands were run.
