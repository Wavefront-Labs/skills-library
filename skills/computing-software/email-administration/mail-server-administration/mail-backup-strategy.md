---
id: computing-software.email-administration.mail-server-administration.mail-backup-strategy
name: mail-backup-strategy
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mail-backup-strategy, mail-backup, backup, doveadm-backup]
level: practitioner
status: draft
description: "Back up mailboxes, Postfix configuration, DKIM keys, TLS certs and user databases with a consistent method."
sources:
  - https://doc.dovecot.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mail backup strategy

**Goal:** a complete, restorable backup set.
## Contents
- Mail storage (Maildir/mdbox), or `doveadm backup` to a second host.
- `/etc/postfix`, `/etc/dovecot`, DKIM private keys, user database dump, `/etc/aliases`.
- Not the Postfix queue (transient), but note deferred mail is lost without it.
## Steps
1. Use filesystem snapshots for consistency, then copy the snapshot.
2. Encrypt the backup and keep an off-site copy.
3. Keep config in version control as well.
## Failure modes
- Backing up mdbox files live yields inconsistent copies.
## Verify
- Perform a restore drill quarterly (see restore-testing).

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
