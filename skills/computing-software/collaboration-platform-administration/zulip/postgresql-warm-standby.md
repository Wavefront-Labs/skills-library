---
id: computing-software.collaboration-platform-administration.zulip.postgresql-warm-standby
name: postgresql-warm-standby
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [warm-standby, wal-g, pg-ctl-promote, replication]
level: sme
status: docs-checked
description: "Build a Zulip PostgreSQL warm standby: replication_user and replication_primary in zulip.conf, wal-g or pg_basebackup, promotion and multi-host REMOTE_POSTGRES_HOST failover."
sources: ["https://zulip.readthedocs.io/en/latest/production/postgresql.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PostgreSQL warm standby for Zulip

A warm standby replica is the documented disaster-recovery option for the database. Zulip's configuration can build on `wal-g`, its streaming backup tool, to create base images without loading the primary, but it is not required.

On the replica, name the primary and the replication account in `/etc/zulip/zulip.conf`:

```
[postgresql]
replication_user = replicator
replication_primary = hostname-of-primary.example.com
```

The `postgres` user on the replica must be able to authenticate as that user, which may need `pg_hba.conf` entries and client certificates. For password authentication, set `postgresql_replication_password` in `/etc/zulip/zulip-secrets.conf`.

Run `zulip-puppet-apply` to rebuild the PostgreSQL configuration. Then fetch a base backup: `env-wal-g backup-fetch` if using wal-g, otherwise `pg_basebackup`. The replica should begin live replication.

On primary failure, run `pg_ctl promote` on the standby. Make sure the old primary cannot return, or the cluster ends up with two diverging timelines.

For faster failover without restarting Zulip services, list both hosts in `/etc/zulip/settings.py`:

```
REMOTE_POSTGRES_HOST = 'primary-database-host,warm-standby-host'
```

Zulip uses the first one that accepts writes and keeps retrying the list in order until a promoted replica becomes writable.

Also watch the `autovac_freeze` check_postgres alert: when it fires, run `VACUUM` in the indicated databases as the `postgres` superuser, before PostgreSQL forces a vacuum, which can cause sudden downtime.

## Checked

Confirmed against the PostgreSQL warm standby and vacuuming alerts sections of the PostgreSQL page: replication_user, replication_primary, the replication password secret, backup-fetch versus pg_basebackup, pg_ctl promote, the comma-separated REMOTE_POSTGRES_HOST and the autovac_freeze alert. Reworded the vacuum consequence to match the page.

Method: docs-checked 2026-11-09 against docs/production/postgresql.md in the zulip/zulip repository (main), the source of the cited page.
