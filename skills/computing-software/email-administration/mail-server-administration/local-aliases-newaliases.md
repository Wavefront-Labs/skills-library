---
id: computing-software.email-administration.mail-server-administration.local-aliases-newaliases
name: local-aliases-newaliases
category: computing-software
field: email-administration
product: mail-server-administration
tags: [local-aliases-newaliases, aliases, newaliases, postmaster]
level: intro
status: docs-checked
description: "Maintain /etc/aliases for local system recipients (postmaster, root) and rebuild with newaliases."
sources:
  - https://www.postfix.org/aliases.5.html
  - https://www.postfix.org/newaliases.1.html
  - https://www.postfix.org/BASIC_CONFIGURATION_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local aliases newaliases

**Goal:** every system mailbox forwards to a human (ALIASES and local(8) docs).
## Steps
1. Edit `/etc/aliases`: `postmaster: admin@example.com` and `root: postmaster`.
2. Rebuild: `newaliases` (or `postalias /etc/aliases`).
3. Confirm the setting: `postconf alias_maps alias_database`.
## Failure modes
- Forgetting `newaliases`: lookups use the old database.
- Delivery to `|command` and /file/name from aliases is disallowed by default (`allow_mail_to_commands`, `allow_mail_to_files`); leave them off unless required.
- No postmaster alias: BASIC_CONFIGURATION_README says to set up a postmaster alias.
## Verify
- `postalias -q postmaster /etc/aliases` prints the target (aliases.5 uses `postalias -q name [file-type]:[file-name]`).
- Send to postmaster@example.com and confirm delivery.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): aliases(5), newaliases(1), BASIC_CONFIGURATION_README.
Confirmed: `newaliases`, `postalias -q`, `alias_maps`, `alias_database`, the postmaster alias advice, `allow_mail_to_commands` default off.
Corrected or removed: the 'run as the alias owner' claim, the RFC 5321 citation (not in the pages read), `postmap -q` on the aliases file (postalias is the documented tool).
Method: documentation only; no commands were run.
