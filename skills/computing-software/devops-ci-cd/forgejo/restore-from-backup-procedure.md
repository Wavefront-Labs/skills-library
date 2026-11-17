---
id: computing-software.devops-ci-cd.forgejo.restore-from-backup-procedure
name: restore-from-backup-procedure
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [restore, backup-restoration, authorized-keys-cron, rebuild-indexer]
level: practitioner
status: docs-checked
description: "Restore Forgejo in the right order and run the admin cron tasks that regenerate SSH keys and indexes."
sources:
  - https://forgejo.org/docs/latest/admin/setup/backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Restoring needs knowledge of how the backup was made and which configuration was in use. The general order is:

1. Restore the database with the matching database tool, or the file-based method for SQLite.
2. Restore the files as backed up, typically the `data` directory, which is the parent of the default repository, storage, queue and indexer locations.
3. Restore app.ini, or rebuild it pointing at the restored file paths.
4. Start Forgejo.

After logging in as an administrator, use the `/admin/monitor/cron` page for maintenance tasks:

- If SSH is used, run the cron jobs that update the `.ssh/authorized_keys` file with Forgejo SSH keys and the `.ssh/authorized_principals` file with SSH principals. Those files are not part of the described backup because Forgejo can regenerate them from database data.
- If the issue indexer was neither backed up nor restored, run the Rebuild issue indexer cron job.
- If the repository indexer was not restored, it rebuilds automatically on startup.

Keep the original `SECRET_KEY` and `JWT_SECRET`: without the first, Forgejo cannot read encrypted values such as webhook credentials; without the second, integrations must reauthenticate.

## Checked

2026-11-04. Confirmed against the Forgejo Backups and Backup Restoration page (Restoring Forgejo and Configuration Settings sections): the four-step order, the three cron-page maintenance tasks, and the SECRET_KEY and JWT_SECRET consequences. Nothing removed.

Method: documentation only; no commands were run.
