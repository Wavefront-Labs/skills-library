---
id: computing-software.database-administration.mysql.in-place-vs-logical-upgrade-and-release-model
name: in-place-vs-logical-upgrade-and-release-model
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-upgrade, in-place-upgrade-mysql, logical-upgrade, lts-release, innovation-release, upgrade-paths, data-dictionary-upgrade, downgrade]
level: advanced
status: draft
description: "Choose between in-place and logical MySQL upgrades, follow supported upgrade paths under the LTS/Innovation release model, and plan a real rollback."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/upgrade-paths.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html
  - https://dev.mysql.com/doc/refman/8.4/en/upgrade-binary-package.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-place vs logical upgrade

**Goal:** pick the upgrade method that fits the data size and downtime budget,
and keep a working path back.

## Release model (since 8.0.34)
- **LTS** (8.4, then 9.7...): ~5 years premier + extended support, only bug/security fixes within the series.
- **Innovation** (9.0, 9.1, ...): quarterly, new features, supported only until the next one.
Production databases normally run LTS. Supported paths: within an LTS series;
LTS → next LTS; LTS → innovation releases before the next LTS. 5.7 → 8.0 → 8.4 (no skipping).

## In-place upgrade
Stop, swap binaries, start; the server upgrades the data dictionary and system
tables itself at startup (8.0.16+, no `mysql_upgrade` step).
1. Run the upgrade checker; fix errors.
2. Take a backup; set `innodb_fast_shutdown = 0` and shut down cleanly (full purge/merge).
3. Install new packages; keep my.cnf free of removed variables.
4. Start; watch the error log for `Server upgrade from '80039' to '80403' completed`.
- Fast (minutes regardless of size). Downgrade of the data dir is **not supported**
  across major/LTS boundaries: rollback = restore backup or fail back to a
  replica still on the old version.

## Logical upgrade
Dump (`mysqlsh util.dumpInstance` or mysqldump) from old, load into a fresh new
server. Slow for big data, but cleans up fragmentation, changes defaults
(charset), and allows platform moves.

## Replica-based (recommended for production)
Upgrade a replica first (in-place or by loading), let it replicate from the old
source (older source → newer replica is supported), soak test read traffic,
then switch over to it. The old source becomes the rollback target only if you
can replicate back: newer → older replication is not supported in general, so
decide the point of no return explicitly.

## Gotchas
- Upgrading with the server stopped uncleanly (`innodb_fast_shutdown=2`) can
  fail redo log format conversion.
- MySQL 8.0 changed default charset to utf8mb4 and collation to
  `utf8mb4_0900_ai_ci`: mixing collations in joins between old and new tables
  causes `Illegal mix of collations` errors.

## Verify
`SELECT VERSION();`, error log upgrade message, and app smoke tests against the upgraded node before switching traffic.
