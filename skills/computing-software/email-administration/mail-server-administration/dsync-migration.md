---
id: computing-software.email-administration.mail-server-administration.dsync-migration
name: dsync-migration
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dsync-migration, doveadm-sync, doveadm-backup, mailbox-migration]
level: advanced
status: docs-checked
description: "Migrate mailboxes between Dovecot servers with doveadm sync or backup, preserving UIDs and flags."
sources:
  - https://doc.dovecot.org/2.3/admin_manual/migrating_mailboxes/
  - https://doc.dovecot.org/main/core/man/doveadm-sync.1/
  - https://doc.dovecot.org/main/core/man/doveadm-mailbox.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dsync migration

**Goal:** move users without losing UIDs/flags.
## Steps
1. Prepare: on the old server add a `service doveadm` `inet_listener` with a port, and set the same `doveadm_password` on both servers (`tcps:` instead of `tcp:` uses SSL).
2. One-way, from the new server (`-R` pulls from the remote): `doveadm backup -R -u alice@example.com tcp:old.example.com`. Run on the old server without `-R`, the destination is the new server. `backup` forces the destination to look exactly like the source, deleting mails and mailboxes if necessary.
3. Repeat while mail still arrives on the old server. After delivery moves, run `doveadm sync -1 -R -u alice@example.com tcp:old.example.com` (one-way, keeps changes already at the destination) to pick up the last mail. Two-way `doveadm sync -u alice@example.com tcp:host` is for when both sides stay in use.
## Failure modes
- Reversing source and target for `backup` destroys data; double-check direction and the `-R` flag.
- Accessing the target mailboxes before the first sync causes GUID or UIDVALIDITY warnings or a failed sync.
- Migration can load the source heavily; there is no throttle.
## Verify
- `doveadm mailbox status -u alice@example.com messages INBOX` equal on both servers.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Migrating Mailboxes page (`doveadm backup -Ru user tcp:host:port`, doveadm_password, destination forced to match source, `sync -1`, caveats) and the doveadm-sync/backup man page (modes, `-R`, `-1`, `tcp:`/`tcps:` destinations, `doveadm_port`) and doveadm-mailbox man page (`mailbox status`). Fixed: the original ran `backup` with the old server as destination, which would have overwritten the old server; the post-cutover pass now uses `sync -1`.

Method: documentation only; no commands were run.
