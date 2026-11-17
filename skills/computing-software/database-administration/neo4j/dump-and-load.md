---
id: computing-software.database-administration.neo4j.dump-and-load
name: dump-and-load
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-admin-dump, neo4j-admin-load, offline-copy, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Community-friendly backups"
sources:
  - https://neo4j.com/docs/operations-manual/current/backup-restore/offline-backup/
  - https://neo4j.com/docs/operations-manual/current/backup-restore/restore-dump/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline dump and load

Goal: back up when offline is acceptable.
- Stop the database, then `neo4j-admin database dump mydb --to-path=...`; load with `neo4j-admin database load`.
- Online backup (`neo4j-admin database backup`) is documented as Enterprise Edition.
Verify: loaded database reports expected counts.

## Checked

2026-11-02. Confirmed in the offline backup page and the online backup page (Enterprise). Removed: the portability-across-versions claim and the `STOP DATABASE` command form (not confirmed).
Method: documentation only; no commands were run.
