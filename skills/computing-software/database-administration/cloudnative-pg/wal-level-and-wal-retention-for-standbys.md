---
id: computing-software.database-administration.cloudnative-pg.wal-level-and-wal-retention-for-standbys
name: wal-level-and-wal-retention-for-standbys
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [wal-level, wal-keep-size, replication-slots, standby, logical, tcp-user-timeout]
level: advanced
status: docs-checked
description: "Decide wal_level (logical by default in CloudNativePG), plan WAL retention so standbys do not fall out of sync, and tune the standby tcp_user_timeout via STANDBY_TCP_USER_TIMEOUT."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**wal_level.** Upstream PostgreSQL defaults to `replica`; CloudNativePG defaults to `logical` so logical replication and migrations work out of the box. Values: `minimal` (crash recovery only), `replica` (WAL archiving, streaming, hot standby reads), `logical` (adds logical decoding information). If you do not need logical replication, set `replica` to reduce WAL volume. `minimal` is allowed only for single-instance clusters with WAL archiving disabled.

**Retention.** Planning WAL segment retention is your duty: configure `wal_keep_size` (default `512MB`) from the expected and observed workload. If the only streaming clients are the cluster's own replicas, enable cluster-level replication slots with `replicationSlots.highAvailability`. Without slots or continuous backup, `wal_keep_size` is the only protection, and a standby that falls behind logs:

```text
could not receive data from WAL stream: ERROR: requested WAL segment ... has already been removed
```

Keeping extra WAL means dedicating part of `PGDATA` (or the WAL volume) to old segments.

**Standby connection settings.** `primary_conninfo`, `restore_command` and `recovery_target_timeline` are managed by the operator and only effective on replicas:

```text
primary_conninfo = 'host=<PRIMARY> user=postgres dbname=postgres tcp_user_timeout=5000'
recovery_target_timeline = 'latest'
```

Every standby uses `tcp_user_timeout` of 5 seconds, controlling how fast a standby abandons an unacknowledged TCP connection. To change it for all standbys, set the operator option `STANDBY_TCP_USER_TIMEOUT`.

## Checked

2026-11-04. wal_level semantics, retention warning and tcp_user_timeout default confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
