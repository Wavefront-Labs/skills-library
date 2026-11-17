---
id: computing-software.database-administration.neo4j.seed-data-and-fixtures
name: seed-data-and-fixtures
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, cypher-seed-script, graph-fixtures, dump-fixtures, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Load Neo4j test fixtures: cypher-shell script files, fail-fast or fail-at-end, and neo4j-admin database dump and load for snapshots"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/docs-operations/blob/dev/modules/ROOT/pages/cypher-shell.adoc", "https://github.com/neo4j/docs-operations/blob/dev/modules/ROOT/pages/backup-restore/restore-dump.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seed data and fixtures

Goal: reproducible test data in a Neo4j database.

- Script seeds as a file of Cypher statements ending in semicolons and run it with `cypher-shell -f <file>` (also `cat seed.cypher | cypher-shell ...` or `:source <file>` in the interactive shell). Add `--format plain` for simple output.
- When reading from a file the shell exits on the first error by default (`--fail-fast`); `--fail-at-end` runs the whole input and reports failures at the end. Prefer the default for seeds so a half-loaded fixture is noticed. Pass values with `-P name=value` if the script is parameterised.
- Make seeds idempotent (`MERGE`, `CREATE CONSTRAINT ... IF NOT EXISTS`) if they may rerun; otherwise reset the database first.
- For large or binary-exact fixtures take a snapshot with `neo4j-admin database dump` and restore with `neo4j-admin database load <database> --from-path=<dir> --overwrite-destination=true`. Replacing a database on a standalone server needs it stopped; on Community Edition `load` only runs against an offline DBMS. Change Data Capture does not capture changes made by `load`.

Verify: after seeding, node and relationship counts are identical on every run.

## Checked
2026-11-09

Method: read the operations-manual source pages cypher-shell and backup-restore/restore-dump (raw asciidoc). Removed: the unsupported generic advice on small deterministic graphs, synthetic performance datasets and version control (not documented in these pages), and the load via cypher-shell wording was made precise. Not checked: neo4j-admin database dump options (offline-backup page).
