---
id: computing-software.database-administration.neo4j.uniqueness-and-existence
name: uniqueness-and-existence
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, unique-constraint, property-existence, create-constraint, constraints, node-key, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Integrity rules"
sources:
  - https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/
  - https://neo4j.com/docs/cypher-manual/current/schema/constraints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uniqueness and existence constraints

Goal: enforce data integrity.
- `CREATE CONSTRAINT person_email IF NOT EXISTS FOR (p:Person) REQUIRE p.email IS UNIQUE`.
- Uniqueness constraints do not require the property to exist: nodes missing it are not subject to the rule. Property existence constraints are labelled Enterprise Edition on the page.
- Uniqueness and key constraints are backed by range indexes; dropping the constraint drops the backing index.
Verify: a duplicate insert fails.

## Checked

2026-11-02. Confirmed: uniqueness syntax, missing-property behaviour, Enterprise label on existence constraints, backing range index and drop behaviour (create-constraints). Removed: 'some editions' vagueness.
Method: documentation only; no commands were run.
