---
id: computing-software.collaboration-platform-administration.zulip.zulip-backup-tool
name: zulip-backup-tool
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [manage-py-backup, backup-contents, skip-db, backup-tarball]
level: practitioner
status: docs-checked
description: "Run Zulip's built-in manage.py backup command with --output, --skip-db and --skip-uploads, and know what the tarball includes and what it leaves out."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The manage.py backup tool

Run as the `zulip` user, or as root through `su`:

```
~zulip/deployments/current/manage.py backup
su zulip -c '~zulip/deployments/current/manage.py backup'
```

Options:

- `--output=/tmp/backup.tar.gz` sets the tarball name (default a file in `/tmp`; the console prints the final path).
- `--skip-db` omits the database, useful with a remote PostgreSQL that has its own backup system.
- `--skip-uploads` ignores user-uploaded files when `LOCAL_UPLOADS_DIR` is set.

The `.tar.gz` holds what is needed to recreate the server on another machine: the database, settings and secrets from `/etc/zulip`, and locally stored uploads.

Not included:

- Server logs in `/var/log/zulip`, which are append-only and can be huge.
- Files in the S3 upload backend, which can dwarf the rest of the backup and have their own backup tooling.
- SSL certificates, since they are sensitive and either trivially replaced (Certbot) or supplied by you.
- Transient state: typing status, rate-limiting counters and RabbitMQ queues that are essentially always empty on a healthy server. Check with `rabbitmqctl list_queues`.

Why configuration matters: if you lose `secret_key` all users must log in again, because cookies cannot be verified, and if you lose `avatar_salt` avatars must be re-uploaded, since filenames hash it with the email.

Handle the tarball as sensitive: it contains the secrets from `/etc/zulip`.

## Checked

Method: docs-checked 2026-11-09 against the Zulip Backups, export and import page (read in full); advice to store the tarball off the server dropped as not on the page.
