---
id: computing-software.devops-ci-cd.forgejo.backup-what-to-save
name: backup-what-to-save
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [backup, forgejo-backup, secret-key, app-ini-backup]
level: practitioner
status: docs-checked
description: "Identify every part of a Forgejo instance that a backup must cover: database, repositories, storage, queues, config, indexers."
sources:
  - https://forgejo.org/docs/latest/admin/setup/backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo recommends no specific backup tool, but it strongly recommends shutting Forgejo down during a backup, because data lives in several systems and a consistent snapshot of a running instance is not trivial.

What to back up:

- Database: for SQLite the file at `[database].PATH`; otherwise use the engine's own tool (mariadb-backup, mysql, or pg_dump).
- Repositories: by default `data/forgejo-repositories` under WORK_PATH, changeable with `[server].APP_DATA_PATH` or `[repository].ROOT`.
- Storage: every configured subsystem directory when local; with minio, the remote object store needs its own backup.
- Queues: the `data/queues` directory when `[queue].TYPE` is level; a persistent redis if TYPE is redis; channel or dummy cannot be backed up.
- app.ini, especially `[security].SECRET_KEY` (encrypts values such as webhook credentials), `[oauth2].JWT_SECRET`, and the SSH host keys when `START_SSH_SERVER` is true.
- Indexers: optional but advisable for large installations, since rebuilding is slow and I/O heavy.
- Logs: not required unless used for analysis.

With SQLite and default paths, backing up the data folder covers the database, repositories, storage, queues and indexers.

## Checked

2026-11-04. Confirmed against the Forgejo Backups and Backup Restoration page: shutdown warning, database tools, repository path and overrides, storage local and minio, queue types, the three app.ini items, indexers and logs. Nothing removed.

Method: documentation only; no commands were run.
