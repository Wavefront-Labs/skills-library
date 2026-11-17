---
id: computing-software.email-administration.mailcow.mailcow-restore-procedure
name: mailcow-restore-procedure
category: computing-software
field: email-administration
product: mailcow
tags: [restore, restore-points, maildir-sub, architecture-mismatch, new-system-restore]
level: advanced
status: docs-checked
description: "Restore mailcow components from a backup_and_restore.sh backup onto a running empty install, including the MAILDIR_SUB and cross-architecture pitfalls."
sources: ["https://docs.mailcow.email/backup_restore/b_n_r-restore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restoring mailcow from backup

To restore on a new system, mailcow must first be installed and running in an empty state. Then run `./helper-scripts/backup_and_restore.sh restore` (do not move the script). It asks for the absolute backup location, lists the `mailcow-<date>` restore points to pick by number, then lists components: 0 all, 1 crypt data, 2 Rspamd data, 3 mail directory, 4 Redis DB, 5 Postfix data, 6 SQL DB. Option 0 restores everything. `THREADS` and `MAILCOW_BACKUP_LOCATION` work as for backup.

Older installations: check whether `MAILDIR_SUB` is set in the old `mailcow.conf`. If it was not set, do not set it in the new one, otherwise no mail will be displayed because Dovecot looks in the wrong directory.

Architecture: a backup from x86 restored to ARM64 (or the reverse) shows Rspamd data as incompatible (`[ NaN ] - Rspamd data (incompatible Arch, cannot restore it)`), and choosing 0 skips Rspamd. Restoration time depends on backup size.

## Checked

2026-11-09. Confirmed on the Restore page: running mailcow in an empty state, script not moved, restore point and component menu 0 to 6, THREADS and MAILCOW_BACKUP_LOCATION, the MAILDIR_SUB warning and the x86 to ARM64 Rspamd incompatibility message. No changes needed.

Method: docs-checked 2026-11-09 against the full Restore page (b_n_r-restore.en.md in mailcow-dockerized-docs).
