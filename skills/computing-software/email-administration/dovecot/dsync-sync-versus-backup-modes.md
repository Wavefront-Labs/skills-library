---
id: computing-software.email-administration.dovecot.dsync-sync-versus-backup-modes
name: dsync-sync-versus-backup-modes
category: computing-software
field: email-administration
product: dovecot
tags: [dsync, doveadm-sync, doveadm-backup, two-way-sync, one-way-sync, replication-modes]
level: practitioner
status: docs-checked
description: "Choose among doveadm backup, sync and sync -1, and understand GUID-based UID conflict handling between source and destination."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-sync.1.html
  - https://doc.dovecot.org/main/core/man/doveadm-backup.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
dsync (doveadm sync) synchronizes mailboxes, makes backups and converts mailboxes between formats. Three modes exist:

- `doveadm backup`: one-way. Changes at the destination are reverted, so the destination ends up identical to the source.
- `doveadm sync`: two-way. All changes merge without loss, and both sides end up identical. Safe for any modifications on both sides.
- `doveadm sync -1`: one-way, but destination changes are preserved and new source changes merged on top. The merge does not work perfectly, so limit its use.

The one-way algorithm matches the two-way one except that the source is not modified. Each message's GUID identifies conflicting UIDs. Example: UIDs 1-5 are backed up, then UID 6 arrives at the source while UID 1 is expunged at the destination; UID 1 stays removed there and UID 6 is copied. If both sides hold different messages with UID 6, headers mismatch and both are kept at the destination with new UIDs 7 and 8 so no client is confused about what UID 6 was.

The goal is that an IMAP or POP3 client cannot tell the two mailboxes apart.

dsync uses the same configuration as Dovecot (via doveconf); override with `-c` or `-o`, including when executing a remote dsync. It can run standalone, needing no server processes unless `-u` triggers a userdb lookup through the auth process. Use `-u` for one user, `-A` for all, or `-F file` for a list; with `-A` and system users from the passwd userdb, beware users below `first_valid_uid`.

## Checked

2026-11-03. Confirmed on the doveadm-sync(1) and doveadm-backup(1) pages: backup is one-way and reverts destination changes, sync is two-way and lossless, sync -1 preserves destination changes and merges imperfectly, the GUID-based conflict example (UID 1..5, UID 6, new UIDs 7 and 8), the aim that IMAP/POP3 clients see no difference, shared Dovecot configuration with -c/-o, standalone use except for -u lookups, and the -A caution about first_valid_uid. Nothing removed.

Method: documentation only; no commands were run.
