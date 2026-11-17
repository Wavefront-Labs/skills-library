---
id: computing-software.collaboration-platform-administration.zulip.wal-g-restore-database
name: wal-g-restore-database
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [wal-g-restore, backup-fetch, recovery-signal, flush-memcached]
level: sme
status: docs-checked
description: "Restore the Zulip PostgreSQL database from wal-g backups: backup-list, stop-server, remove data directory, backup-fetch LATEST, recovery.signal and flush-memcached."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restoring from wal-g backups

Warning: this deletes your current database and restores the latest backup.

1. As root on the database host, list backups; the latest is at the bottom and is what will be restored:

```
env-wal-g backup-list --pretty
```

2. On the application host (which may be a different machine), stop Zulip:

```
~zulip/deployments/current/scripts/stop-server
```

3. As root on the database host stop PostgreSQL: `service postgresql stop`.
4. As root on the database host, delete the database and fetch the backup. This can take a while depending on size and bandwidth:

```
pg_version=$(crudini --get /etc/zulip/zulip.conf postgresql version)
rm -rf "/var/lib/postgresql/$pg_version/main"
env-wal-g backup-fetch "/var/lib/postgresql/$pg_version/main" LATEST
chown -R postgres.postgres "/var/lib/postgresql/$pg_version/main"
touch "/var/lib/postgresql/$pg_version/main/recovery.signal"
service postgresql start
```

5. As root on the application host, flush caches and start Zulip:

```
~zulip/deployments/current/scripts/setup/flush-memcached
~zulip/deployments/current/scripts/start-server
```

## Checked

Confirmed against the Restoring from wal-g backups section of the export-and-import page: every step and command, including the crudini lookup, backup-fetch LATEST, recovery.signal, flush-memcached and start-server. Removed two explanatory sentences about WAL replay and memcached (not on the page).

Method: docs-checked 2026-11-09 against docs/production/export-and-import.md in the zulip/zulip repository (main), the source of the cited page.
