---
id: computing-software.systems-network-administration.immich.borg-backup-script
name: borg-backup-script
category: computing-software
field: systems-network-administration
product: immich
tags: [borg, cron, offsite, pg-dump, deduplication]
level: practitioner
status: docs-checked
description: "Template Borg script that dumps the Immich database next to the library, backs both up locally and to a remote host, prunes and restores with borg mount."
sources:
  - https://docs.immich.app/guides/template-backup-script
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a cron-driven, versioned backup of the database and library together with Borg.

Prerequisites: Borg on the server and the remote host; optionally your user in the docker group; passwordless ssh to the remote for non-interactive runs.

One-time setup:

```bash
UPLOAD_LOCATION="/path/to/immich/directory"
BACKUP_PATH="/path/to/local/backup/directory"
REMOTE_HOST="remote_host@IP"
REMOTE_BACKUP_PATH="/path/to/remote/backup/directory"
mkdir "$UPLOAD_LOCATION/database-backup"
borg init --encryption=none "$BACKUP_PATH/immich-borg"
borg init --encryption=none "$REMOTE_HOST:$REMOTE_BACKUP_PATH/immich-borg"
```

Scheduled script (add to crontab):

```bash
docker exec -t immich_postgres pg_dump --clean --if-exists --dbname <DB_DATABASE_NAME> --username=<DB_USERNAME> > "$UPLOAD_LOCATION"/database-backup/immich-database.sql
borg create "$BACKUP_PATH/immich-borg::{now}" "$UPLOAD_LOCATION" --exclude "$UPLOAD_LOCATION"/thumbs/ --exclude "$UPLOAD_LOCATION"/encoded-video/
borg prune --keep-weekly=4 --keep-monthly=3 "$BACKUP_PATH"/immich-borg
borg compact "$BACKUP_PATH"/immich-borg
```

Repeat the `create`, `prune` and `compact` lines against `$REMOTE_HOST:$REMOTE_BACKUP_PATH/immich-borg` for the off-site copy. Paths must not contain `:`, `@` or `"`.

Do not gzip the dump for Borg or Restic: compressing can increase backup size by making deduplication harder. If you still prefer to compress, the docs use `gzip --rsyncable`.

Because the dump sits in the upload folder, the database and assets are snapshotted together, so you can turn off Immich's built-in automatic database backups to save space.

Restore: `mkdir /tmp/immich-mountpoint`, `borg mount "$BACKUP_PATH"/immich-borg /tmp/immich-mountpoint`, copy files out of the snapshot sub-directories, then `borg umount /tmp/immich-mountpoint`.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: guides/template-backup-script (all sections).
Removed or reworded: the absolute statement about compression.
Method: documentation only; no commands were run.
