---
id: computing-software.email-administration.mailcow.mailcow-accidental-mailbox-deletion-recovery
name: mailcow-accidental-mailbox-deletion-recovery
category: computing-software
field: email-administration
product: mailcow
tags: [accidental-deletion, mailbox-recovery, maildir-gc-time, sogo-tool-restore, garbage-folder, doveadm-resync]
level: advanced
status: docs-checked
description: "Recover a deleted mailbox from the _garbage folder and its SOGo groupware data from the daily SOGo user-data backups."
sources: ["https://docs.mailcow.email/backup_restore/b_n_r-accidental_deletion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recovering an accidentally deleted mailbox

Mail: a deleted mailbox is kept in encrypted form for `MAILDIR_GC_TIME` (default 5 days, set in `mailcow.conf`) under the vmail volume's `_garbage` folder, in a directory named `[timestamp]_[domain_sanitized][user_sanitized]`, for example `1629109708_exampleorgtest`. Re-create the user first, then copy the folders back to `[domain]/[user]` in the vmail volume. Restore to the same mailcow or use the same keys from `crypt-vol-1`. Then run `doveadm force-resync -u user@example.net '*'` and `doveadm quota recalc -u user@example.net` inside `dovecot-mailcow` (via `docker compose exec`).

SOGo data (calendars, contacts): daily backups, on a 24 hour interval starting when the stack is brought up, go into the `sogo-userdata-backup-vol-1` volume. Make sure the user exists, copy the file named after the user into `data/conf/sogo`, then run `docker compose exec -u sogo sogo-mailcow sogo-tool restore -F ALL /etc/sogo user@example.org`. Run `sogo-tool` without parameters for other restore options. Delete the copied file afterwards and restart with `docker compose restart sogo-mailcow memcached-mailcow`.

The docs say this works if the mistake is noticed within a few hours.

## Checked

2026-11-04. Confirmed on the Recover accidentally deleted data page: the few-hours caveat, SOGo daily backups on a 24 hour interval into sogo-userdata-backup-vol-1, the copy to data/conf/sogo, the sogo-tool restore command, restarting sogo-mailcow and memcached-mailcow, MAILDIR_GC_TIME default 5 days, the _garbage folder naming example, the same-mailcow or crypt-vol-1 key requirement, and the doveadm force-resync and quota recalc commands. No changes needed.

Method: documentation only; no commands were run.
