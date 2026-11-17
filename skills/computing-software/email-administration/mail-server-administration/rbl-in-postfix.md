---
id: computing-software.email-administration.mail-server-administration.rbl-in-postfix
name: rbl-in-postfix
category: computing-software
field: email-administration
product: mail-server-administration
tags: [rbl-in-postfix, reject-rbl-client, reject-rhsbl-sender, rbl]
level: practitioner
status: docs-checked
description: "Use reject_rbl_client and reject_rhsbl_sender in Postfix carefully, and prefer scoring or postscreen for big lists."
sources:
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/SMTPD_ACCESS_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rbl in postfix

**Goal:** apply blocklists without blocking real mail.
## Steps
1. `smtpd_recipient_restrictions = ..., reject_rbl_client zen.example.org` (placed after permit rules for your own users).
2. Add `reject_rhsbl_sender dbl.example.org` for domain lists.
3. Read each list's usage policy and volume limits before using it.
## Failure modes
- A single large list false-positive affecting a customer; keep an exception via `check_client_access`.
## Verify
- Test with the list's published test address and confirm the RCPT is rejected.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) reject_rbl_client, reject_rhsbl_sender; SMTPD_ACCESS_README.
Confirmed: `reject_rbl_client`, `reject_rhsbl_sender`, `check_client_access` exceptions.
Corrected or removed: the resolver advice and the 127.0.0.2 test address (list-specific, not in the pages read).
Method: documentation only; no commands were run.
