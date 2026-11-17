---
id: computing-software.data-engineering.kestra.backup-restore
name: backup-restore
category: computing-software
field: data-engineering
product: kestra
tags: [backup, restore, pg-dump, internal-storage, maintenance-mode, migration]
level: advanced
status: docs-checked
description: "Back up and restore Kestra: database dumps for PostgreSQL and MySQL, internal storage, the Enterprise metadata backup command, and moving storage backends."
sources:
  - https://kestra.io/docs/administrator-guide/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three things to back up: metadata (Enterprise only), the database, and internal storage. Kestra does not back up internal storage itself.

JDBC database: stop Kestra before backing up and restart after restoring.

```bash
pg_dump -h localhost -p 5432 -U <username> -d <database> -F tar -f kestra.tar
pg_restore -h localhost -p 5432 -U <username> -d <database> kestra.tar
mysqldump -h localhost -P 3306 -u <username> -p'<password>' <database> > kestra.sql
```

Internal storage: filesystem tools for local; provider replication for managed object storage; Restic and/or replication for self-hosted (Ceph, SeaweedFS).

Enterprise metadata backup (enable Maintenance Mode first):

```bash
kestra backups create FULL
kestra backups restore kestra:///backups/full/backup-20240917163312.kestra
```

Options: `--tenant`, `--encryption-key`, `--no-encryption`, `--include-data`, `--to-tenant`. `LOG` and `METRIC` records are inserted, so re-running a restore duplicates them.

Elasticsearch with Kafka: snapshot and restore `kestra_*` indices, then on a fresh Kafka run `kestra sys-ee restore-queue`. Some in-flight state exists only in Kafka.

Moving storage backends: stop Kestra, sync objects and folder markers (keys ending `/`), compare counts, update `kestra.storage` with identical keys, start and verify. Roll back only before any flows run on the new backend.

## Checked

2026-11-04. Confirmed against the Kestra backup and restore page: Enterprise-only metadata backup, kestra backups create FULL and restore commands, options --tenant, --encryption-key, --no-encryption, --include-data, --to-tenant, LOG and METRIC duplicate on re-run, pg_dump, pg_restore and mysqldump forms, internal storage guidance, Elasticsearch with Kafka restore-queue, storage migration steps and rollback. Nothing removed.

Method: documentation only; no commands were run.
