---
id: computing-software.database-administration.neo4j.upgrade-planning
name: upgrade-planning
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, upgrade-path, migrate-configuration, pre-upgrade-checks, neo4j-upgrade, version-compatibility, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Plan a Neo4j upgrade: migrate the legacy config with neo4j-admin, match GDS versions, and for Aura move a Neo4j 4 snapshot to a new instance."
sources: ["https://neo4j.com/docs/operations-manual/current/configuration/migrate-configuration/", "https://neo4j.com/docs/operations-manual/current/configuration/plugins/", "https://neo4j.com/docs/aura/tutorials/upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade planning

Goal: upgrade safely.
- Read the upgrade and migration guide for your exact source and target versions before touching anything.
- Self-managed: migrate the legacy configuration with `bin/neo4j-admin server migrate-configuration --from-path=<old conf dir> --to-path=<new conf dir>`. It writes the new format, renames originals when source and target directories are the same, and reports settings that could not be migrated. Inspect the output rather than copying it. Settings passed with `--additional-config` are not migrated.
- Plugins: GDS has its own supported-versions table, so check it and pick the GDS release that matches the new Neo4j version (see the Configure plugins page).
- Aura: from a Neo4j 4 instance, export a snapshot dump, create a Neo4j 5 instance, and import the dump into it.
- Back up and rehearse on a copy first.
Verify: application smoke tests pass against the copy before the real upgrade.

## Checked

2026-11-09. Confirmed against the operations manual Migrate configurations and Configure plugins pages (docs-operations) and the Aura upgrade tutorial (docs-aura tutorials/upgrade). Removed: "Neo4j 4.x to 5.x changed config names and procedures" (not stated on these pages), "upgrade clusters per documented rolling procedure" (cluster upgrade steps were not checked), the APOC version claim, and the draft disclaimer. Backup-and-rehearse is practice advice.

Method: documentation only; no commands were run.
