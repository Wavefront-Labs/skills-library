---
id: computing-software.collaboration-platform-administration.zulip.manual-backup-and-restore
name: manual-backup-and-restore
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [manual-backup, no-init-db, configure-rabbitmq, secret-key]
level: advanced
status: docs-checked
description: "Back up and restore Zulip pieces by hand: PostgreSQL, uploads, /etc/zulip secrets, install --no-init-db and configure-rabbitmq for remote-database setups."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual backups and restores

Use this when you manage backups yourself, for example with a remote PostgreSQL that already has a backup regime.

What to back up:

- The PostgreSQL database, using any standard export or backup tool.
- User uploads. In S3 they are already stored there. With `LOCAL_UPLOADS_DIR`, back up that directory, avatars included.
- The configuration and secrets in `/etc/zulip/`. Losing `secret_key` forces every user to log in again; losing `avatar_salt` forces avatar re-uploads, because avatar file names derive from a hash of it and the email.

Restore is the reverse:

1. Install a new server from a release tarball with `scripts/setup/install`, passing `--no-init-db` since no new database is wanted.
2. Unpack `settings.py` and `zulip-secrets.conf` from your backups into `/etc/zulip`.
3. Restore the database from the backup.
4. As root run `scripts/setup/configure-rabbitmq` to set RabbitMQ's password from the secrets file.
5. If you use local uploads, restore the files to the `LOCAL_UPLOADS_DIR` path, and logs if appropriate.
6. Start with `scripts/restart-server`.

The same procedure migrates an installation to a new server.

Recommendation from the documentation: run a disaster recovery test once backups exist. Remember that wal-g database backups alone are not a full system backup; configuration, secrets and local uploads still need coverage.

## Checked

Method: docs-checked 2026-11-09 against the Zulip Backups, export and import page (read in full).
