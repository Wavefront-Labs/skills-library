---
id: computing-software.database-administration.cockroachdb.rolling-upgrade-and-finalization
name: rolling-upgrade-and-finalization
category: computing-software
field: database-administration
product: cockroachdb
tags: [upgrade, rolling-upgrade, finalization, rollback, auto-upgrade]
level: practitioner
status: docs-checked
description: "Upgrade self-hosted CockroachDB node by node: patch versus major upgrades, auto-finalization, the version cluster setting, disabling auto-finalization, rollback."
sources:
  - https://www.cockroachlabs.com/docs/stable/upgrade-cockroach-version
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upgrade a cluster without downtime and keep the option to roll back until you finalize.

Patch upgrade (same major version), one node at a time: replace the `cockroach` binary (or container image), restart, verify the node rejoined, then confirm it accepts SQL:
```shell
cockroach sql -e 'select 1'
```
Unless a node has tens of thousands of ranges, about one minute is usually enough.

Major-version upgrade: same per-node procedure with the new major binary. By default auto-finalization is enabled and starts as soon as the last node rejoins; after finalization begins you can no longer roll back to the previous major version. The page also lists a license-key check as prepare step.

Keep control of finalization: set `cluster.auto_upgrade.enabled` to `false` before upgrading (the older approach was `cluster.preserve_downgrade_option`; either blocks auto-finalization). Then test, and either roll back or finalize.

Manual finalize:
```sql
SET CLUSTER SETTING version = '{VERSION}';  -- the new major version
SHOW CLUSTER SETTING version;               -- confirm it moved
```
Migration jobs (named like `26.3-{migration-id}` for 26.3) run and can be monitored in the DB Console. Finalization is not complete until all schema change jobs reach a terminal state, so it can take as long as the longest one. If the version does not advance with auto-finalization enabled, look for decommissioning nodes whose decommission has stalled.

Rollback before finalization: repeat the rolling procedure with the previous major version binary; no finalization is needed.

Confirm with `SHOW CLUSTER SETTING version;`; if it still reports the previous version, finalization has not completed.

## Checked

2026-11-03. Confirmed against the upgrade page (published stable page): patch and major procedures, one minute readiness note, license-key check, auto-finalization default, `cluster.auto_upgrade.enabled`, `cluster.preserve_downgrade_option`, manual finalize, migration job names, terminal-state note, stalled decommission, rollback. Removed: restore-from-backup claim and the generic job-name pattern.
Method: documentation only; no commands were run.
