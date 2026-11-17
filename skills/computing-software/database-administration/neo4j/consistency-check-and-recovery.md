---
id: computing-software.database-administration.neo4j.consistency-check-and-recovery
name: consistency-check-and-recovery
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-admin-check, store-copy, db-recovery, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Repairing storage"
sources: ["https://neo4j.com/docs/operations-manual/current/backup-restore/consistency-checker/", "https://neo4j.com/docs/operations-manual/current/backup-restore/copy-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistency check and recovery

Goal: check and rebuild stores.
- `neo4j-admin database check <database>` checks the consistency of a database, a dump, or a full recovered backup (`--from-path` for a dump or backup location).
- `neo4j-admin database copy` (Enterprise Edition) creates a compacted, defragmented copy, can clean up inconsistencies, and can migrate directly from 4.4 to any 5.x version.
- `copy` can leave data out with options such as `--ignore-nodes-with-labels`, `--copy-only-nodes-with-labels` and `--skip-labels`; the two label filters cannot be combined.
- `copy` keeps node IDs unless `--compact-node-store` is used; relationships get new IDs.
Verify: a follow-up `neo4j-admin database check` reports no inconsistencies.

## Checked

2026-11-02. Confirmed in the consistency checker page and the copy-database page. Removed: the 'offline' wording and 'keep a backup' advice (not on those pages).
Method: documentation only; no commands were run.
