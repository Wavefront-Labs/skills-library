---
id: computing-software.database-administration.mysql.replication-version-compatibility
name: replication-version-compatibility
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, replication-version-compatibility, mixed-version-replication, rolling-upgrade, binlog-compatibility, mysql-upgrade]
level: practitioner
status: docs-checked
description: "Know which MySQL version combinations can replicate (older source to newer replica), what breaks in mixed-version topologies, and how long to run them."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-compatibility.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-upgrade.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replication compatibility between versions

## The rule
MySQL supports replication from an **older source to a newer replica** for the version combinations where an upgrade
from the source version to the replica version is supported (see the upgrade-paths rules: no skipping an LTS series).
Newer source to older replica might work but is generally not supported.

## Why newer-to-older breaks
- The binary log format can change between major releases. Optional features on the source can be unreadable to older
  replicas: for example binary log transaction compression cannot be read by a replica older than MySQL 8.0.20.
- Statement-based replication fails if statements use SQL features the replica lacks. If both sides support
  row-based replication and no DDL depends on newer features, row-based replication can still carry the data changes.
- Older source to newer replica can fail when the source uses statements or behaviour no longer supported on the replica.

## Upgrade order (rolling)
1. Upgrade all replicas first (farthest from the source first, bottom-up in multi-level topologies), each with the
   normal single-server procedure, then restart replication with `START REPLICA`.
2. Switch over: stop client updates on the source, wait for a replica to apply everything, make that replica the source.
3. Upgrade the old source and reinsert it as a replica.
Keep the mixed period short and avoid DDL or new-feature use during it.

## Downgrade order
Downgrade the source first, then the replicas; on each replica make sure the binary log and relay log are fully
processed and purge them before downgrading.

## Practical checks
```sql
SELECT @@version, @@binlog_format;
```
Run on source and replicas. In the pre-check, MySQL Shell's `util.checkForServerUpgrade()` finds configuration and
stored data that will not work on the target release.

## Gotchas
- In multi-source setups (including chained or circular), more than two MySQL Server versions at once is not
  supported, however many servers there are.
- Use the most recent release in a series; replication capabilities keep improving.
- The server version is recorded in the binary log per transaction (`original_server_version`,
  `immediate_server_version`), which helps trace where a transaction came from.
- Replicas upgraded first let you test the new version under real replicated load before cutover.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual: Replication Compatibility Between MySQL Versions (19.5.2) and
Upgrading or Downgrading a Replication Topology (19.5.3): older-to-newer rule, 8.0.20 compression note, two-version
multi-source limit, upgrade and downgrade order, `original_server_version` / `immediate_server_version`. Removed as
unconfirmed: collation and authentication default examples, the Group Replication mixed-version behaviour and its
override variable, MariaDB remarks, and the unsupported 8.0-to-5.7 rollback tip.
Method: documentation only; no commands were run.
