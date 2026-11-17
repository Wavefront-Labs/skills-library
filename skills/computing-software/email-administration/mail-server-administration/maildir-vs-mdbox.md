---
id: computing-software.email-administration.mail-server-administration.maildir-vs-mdbox
name: maildir-vs-mdbox
category: computing-software
field: email-administration
product: mail-server-administration
tags: [maildir-vs-mdbox, dovecot-mailbox, maildir, mdbox, sdbox, mailbox-format]
level: practitioner
status: docs-checked
description: "Choose between Maildir and mdbox (dbox) storage, with trade-offs for backup, file counts and tooling."
sources:
  - https://doc.dovecot.org/2.3/admin_manual/mailbox_formats/dbox/
  - https://doc.dovecot.org/main/core/man/doveadm-purge.1/
  - https://doc.dovecot.org/main/core/man/doveadm-sync.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maildir vs mdbox

**Goal:** pick the format deliberately (Dovecot mailbox formats docs).
## Facts
- Maildir: one file per message.
- sdbox: Dovecot native, one message per file. mdbox: multiple messages per file (size set by `mdbox_rotate_size`); expunging only lowers a refcount, and `doveadm purge` frees the space (typically a nightly job).
- dbox keeps flags and keywords only in index files, which cannot be regenerated without data loss.
## Steps
1. Maildir: `mail_location = maildir:~/Maildir`.
2. mdbox: `mail_location = mdbox:~/mdbox`, schedule `doveadm purge -A`.
3. Convert per user with dsync, for example `doveadm sync -u alice@example.com mdbox:~/mdbox`, run twice so the second pass applies changes made during the first.
## Failure modes
- Losing dbox index files loses flags and keywords: back up indexes with the mail data, or use `doveadm backup`.
## Verify
- `doveadm mailbox list -u alice@example.com` and `doveadm fetch -u alice@example.com text mailbox INBOX all | head`.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 dbox page (sdbox vs mdbox, refcount and purge, mdbox_rotate_size, index warning), the doveadm-purge man page (`purge -A`) and the doveadm-sync man page (conversion example, backups). Removed: the easy-to-rsync and many-small-files remarks and the live-backup inconsistency claim, neither stated in the docs.

Method: documentation only; no commands were run.
