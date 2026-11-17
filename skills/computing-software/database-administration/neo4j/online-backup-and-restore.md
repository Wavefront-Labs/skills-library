---
id: computing-software.database-administration.neo4j.online-backup-and-restore
name: online-backup-and-restore
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-admin-database-backup, backup-chain, restore-from-backup, neo4j-admin-backup, dump-load, restore, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Enterprise backups"
sources:
  - https://neo4j.com/docs/operations-manual/current/backup-restore/online-backup/
  - https://neo4j.com/docs/operations-manual/current/backup-restore/restore-backup/
  - https://neo4j.com/docs/operations-manual/current/backup-restore/consistency-checker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online backup and restore

Goal: back up a live database.
- Online backup is an Enterprise Edition feature: `neo4j-admin database backup --to-path=/backups mydb`. The server needs `server.backup.enabled` (true by default) and `server.backup.listen_address` (default port 6362).
- Backups can be full or differential; `neo4j-admin backup aggregate` combines a chain.
- Restore: `neo4j-admin database restore --from-path=... mydb`, then run `CREATE DATABASE` against `system` unless you replaced an existing database.
- `neo4j-admin database check` checks a database, a dump or a full recovered backup; it does not support differential or unrecovered full backups.
Verify: restore to a scratch server and compare counts.

## Checked

2026-11-02. Confirmed in the online backup, restore backup, aggregate and consistency checker pages. Removed: the unsupported-by-page hedges.
Method: documentation only; no commands were run.
