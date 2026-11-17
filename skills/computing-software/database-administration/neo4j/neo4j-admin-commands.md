---
id: computing-software.database-administration.neo4j.neo4j-admin-commands
name: neo4j-admin-commands
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-admin-server, neo4j-admin-database, neo4j-admin-memory, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Admin tool"
sources: ["https://neo4j.com/docs/operations-manual/current/neo4j-admin-neo4j-cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# neo4j-admin overview

Goal: know the admin entry points.
- `neo4j-admin server memory-recommendation` and `neo4j-admin server report` are server commands; the `neo4j-admin database` commands are `backup`, `check`, `copy`, `dump`, `import`, `load`, `migrate` and `restore`.
- `neo4j-admin server report` collects information about the deployment into an archive (ZIP/TAR) for remote assessment.
- Admin tasks read `neo4j.conf`. Override order, highest first: `--additional-config`, the command-specific file (for example `neo4j-admin-database-check.conf`), `neo4j-admin.conf`, `neo4j.conf`.
- Run `neo4j-admin database backup` and `restore` as the `neo4j` OS user so file permissions are correct.
- `--help` or `-h` works at every level (`neo4j-admin database --help`).
Verify: `neo4j-admin database --help` lists the subcommands above.

## Checked

2026-11-02. Confirmed in the Neo4j Admin and Neo4j CLI page (command tables, configuration priority, help), the memory-recommendation and report pages, and the online backup and restore pages (invoke as the neo4j user). Removed: `server validate`, and the general ownership claim for all commands.
Method: documentation only; no commands were run.
