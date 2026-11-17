---
id: computing-software.database-administration.yugabytedb.ysql-major-version-upgrade
name: ysql-major-version-upgrade
category: computing-software
field: database-administration
product: yugabytedb
tags: [ysql-major-upgrade, pg-upgrade, postgresql-15, upgrade, yugabyte-upgrade, finalize-upgrade, rollback]
level: sme
status: docs-checked
description: "Run the online YSQL major upgrade from PostgreSQL 11 to 15: superuser setup, extension removal, pg_upgrade --check, mixed-mode flag, catalog upgrade, finalize."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/ysql-major-upgrade-local.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YSQL major version upgrade (PG11 to PG15), manual

Upgrades from a PostgreSQL 11 based version (anything before v2.25) to a PostgreSQL 15 based one (v2025.1 or later stable, v2.25 or later preview). The upgrade is fully online with uninterrupted reads and writes, but all DDL except temporary tables and REFRESH MATERIALIZED VIEW is blocked for the duration, including the monitor phase. Upgrade all client drivers first (they work with both versions). The cluster must already run v2024.2.3.0 or later. CDC with logical replication needs additional steps.

Before you begin:
1. With dedicated YB-Master nodes, create a superuser `yugabyte_upgrade` and put its credentials in `.pgpass` on each master; remove it afterwards.
2. If PITR is enabled, delete its configuration and recreate it after the upgrade is finalized or rolled back.
3. Drop the `pg_stat_monitor` extension (re-create after finalizing). From v2024.2 with pgvector, export the data, drop those tables and `vector`, and recreate after finalizing.
4. Precheck with the `pg_upgrade` shipped in `postgres/bin` of v2025.2 or later: `pg_upgrade --check -U <superuser_name> --old-host <any_yb_node_address> --old-port <port> --old-datadir <yb_data_dir>`. If it flags extensions as incompatible, drop them and re-run; re-enable after finalizing.
5. Back up the cluster.

Upgrade phase:
1. Mixed mode: set the `ysql_yb_major_version_upgrade_compatibility` flag to `11` on every YB-Master and YB-TServer, for example `yb-ts-cli set_flag --server_address <host>:<rpc_port> ysql_yb_major_version_upgrade_compatibility 11` (the page uses ports 7100 and 9100 for the two process types).
2. Upgrade the YB-Masters one at a time (flag stays 11).
3. Upgrade the YSQL catalog: `yb-admin --master_addresses <master_addresses> upgrade_ysql_major_version_catalog`.
4. Upgrade the YB-TServers one at a time (flag stays 11) and watch applications closely.
5. Disable mixed mode by setting the flag back to `0` on all processes, which re-enables pushdown optimizations.

Monitor phase: stay at most about two days (recommended maximum). DDL is still blocked, new features needing format changes are unavailable and no other upgrade can start.

Finalize: `yb-admin --master_addresses <master_addresses> finalize_upgrade` (cluster-level, run once).

Rollback (before finalizing): set the flag to 11 everywhere, roll back the YB-TServers, run `yb-admin --master_addresses <master_addresses> rollback_ysql_major_version_catalog`, roll back the YB-Masters to v2024.2.3.0, run ANALYZE if you use the cost-based optimizer, then set the flag back to 0. Backups taken in the monitor phase can only be restored on a PG15 compatible universe.

After finalizing, run ANALYZE if you use the cost-based optimizer. Expression pushdown is only partially available during this upgrade.

## Checked

2026-11-09: prerequisites, extension handling, precheck command, mixed-mode flag, upgrade order, catalog commands, finalize, rollback order, the two-day monitor limit and the limitations confirmed against the manual YSQL major upgrade page (yugabyte-db docs manage/ysql-major-upgrade-local.md, read in full). Corrected the availability claim (the cluster must run v2024.2.3.0 or later; the target is a PG15 based release) and the pgvector condition (applies when upgrading from v2024.2).

Method: docs-checked 2026-11-09 against yugabyte-db docs manage/ysql-major-upgrade-local.md
