---
id: computing-software.email-administration.mail-server-administration.imapsync-migration
name: imapsync-migration
category: computing-software
field: email-administration
product: mail-server-administration
tags: [imapsync-migration, mail-migration, imapsync, imap-migration]
level: practitioner
status: draft
description: "Copy mailboxes between IMAP servers with imapsync, with dry runs, folder mapping and repeatable passes."
sources:
  - https://doc.dovecot.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Imapsync migration

**Goal:** move mail from any IMAP server to your Dovecot.
## Steps
1. Dry run first: `imapsync --host1 old.example.net --user1 alice --host2 mail.example.com --user2 alice@example.com --ssl1 --ssl2 --dry` (passwords via `--password1`/`--passfile1`).
2. Run for real; then repeat after cutover to pick up late mail.
3. Check folder mapping options (`--f1f2`, `--regextrans2`) for different hierarchies.
## Failure modes
- Rate limits at the source provider.
- Duplicate messages if run against the same destination from different tools.
## Verify
- Compare message counts per folder on both sides.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
