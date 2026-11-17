---
id: computing-software.database-administration.patroni.patroni-major-version-upgrade
name: patroni-major-version-upgrade
category: computing-software
field: database-administration
product: patroni
tags: [patroni, pg-upgrade, major-upgrade, initialize-key, dcs]
level: advanced
status: docs-checked
description: "The documented procedure for a PostgreSQL major upgrade under Patroni using pg_upgrade."
sources:
  - https://patroni.readthedocs.io/en/latest/existing_data.html
  - https://patroni.readthedocs.io/en/latest/pause.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upgrade the Postgres major version without confusing Patroni.

The documented way is:
1. Stop Patroni.
2. Upgrade PostgreSQL binaries and run `pg_upgrade` on the primary node.
3. Update patroni.yml.
4. Remove the `initialize` key from the DCS, or wipe the complete cluster state with `patronictl remove cluster-name`. This is necessary because pg_upgrade runs initdb, which creates a database with a new system identifier.
5. If you wiped the state, you may copy `patroni.dynamic.json` from the old data directory to the new one to retain PostgreSQL parameters you had set.
6. Start Patroni on the primary.
7. On standbys: upgrade binaries, update patroni.yml and wipe `data_dir`.
8. Start Patroni on the standbys and wait for replication to complete.

Running pg_upgrade on standby nodes is not supported by PostgreSQL. If you know what you are doing, the rsync procedure in the PostgreSQL pg_upgrade documentation can replace wiping data_dir, but the safest way is to let Patroni replicate the data.

Pause mode is described by Patroni as the mechanism for activities like major upgrades, where nodes are stopped, started or promoted outside Patroni's expectations.

## Checked

2026-11-08. Confirmed against the Patroni "Convert a Standalone to a Patroni Cluster" page (major upgrade section) and the pause/resume page (goal section). Removed the FAQ sentence about system identifier mismatches, which is not on the cited pages.

Method: documentation only; no commands were run.
