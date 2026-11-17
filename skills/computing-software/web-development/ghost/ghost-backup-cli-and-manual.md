---
id: computing-software.web-development.ghost.ghost-backup-cli-and-manual
name: ghost-backup-cli-and-manual
category: computing-software
field: web-development
product: ghost
tags: [ghost, backup, ghost-cli, mysqldump, docker, restore]
level: practitioner
status: docs-checked
description: "Back up Ghost with ghost backup, or manually with mysqldump and a tarball of the content folder, including Docker installs."
sources:
  - https://github.com/TryGhost/docs/blob/main/ghost-cli.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/manual-backup.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have a restorable copy before any update.

`ghost backup` writes a zip containing your content as JSON, a member CSV export, installed themes (including the active one), images, files and media, and copies of `routes.yaml` and the redirects file.

The Ghost Admin export is good for moving content but does not include comments, member activity history or media files. For disaster recovery or exact replication, back up the database and content folder directly.

Database:
- Docker: `docker exec <mysql container> mysqldump -u root -p ghost > ~/ghost-backups/ghost_backup.sql`.
- CLI install: `mysqldump -u <ghost_user> -p <database> > ~/ghost-backups/ghost_backup.sql` (credentials are in `config.production.json`).

Content folder:
- CLI install: `cd /var/www/ghost && tar czf ~/ghost-backups/ghost_content_backup.tar.gz content/`.
- Docker: run a temporary alpine container that mounts the Ghost data volume and a backup directory, and tar the volume contents.

Copy backups off the server with `rsync -av` or `scp -r`.

Verify: list the archive (`tar tzf`) and check the SQL dump is non-empty.

## Checked

2026-11-04. Confirmed: ghost backup contents, Admin export limitations, mysqldump commands for Docker and CLI installs, tar commands, temporary alpine container, rsync and scp (Ghost CLI and manual backup pages). Removed: the SQLite stop-before-copy note, which neither page states.

Method: documentation only; no commands were run.
