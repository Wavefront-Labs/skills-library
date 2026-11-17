---
id: computing-software.database-administration.neo4j.migration-tooling
name: migration-tooling
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, schema-migration, constraints, if-not-exists, idempotent, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Version Neo4j schema changes as idempotent CREATE CONSTRAINT IF NOT EXISTS statements that are safe to re-run on every deploy."
sources: ["https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration tooling

Goal: version schema changes.
- Store constraint creation as `CREATE CONSTRAINT <name> IF NOT EXISTS FOR ... REQUIRE ...` statements. With `IF NOT EXISTS`, no error is thrown and nothing is created when a constraint with that name, or the same constraint type and schema, already exists. For property type constraints the property type must also match.
- Give every constraint an explicit name so reruns and later drops are unambiguous.
- Record applied versions in the graph or a tool-managed node, and run the migration on deploy before the application starts.
Verify: re-running the whole set is a no-op.

## Checked

2026-11-09. Confirmed against the Cypher Manual Create constraints page (docs-cypher schema/constraints/create-constraints): IF NOT EXISTS semantics and its example. Removed: the draft disclaimer; index statements are not covered by this page and are not claimed. The version-recording and run-before-start steps are practice advice, not documented behaviour.

Method: documentation only; no commands were run.
