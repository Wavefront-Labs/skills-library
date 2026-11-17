---
id: computing-software.email-administration.mail-server-administration.access-maps-tables
name: access-maps-tables
category: computing-software
field: email-administration
product: mail-server-administration
tags: [access-maps-tables, check-client-access, check-sender-access, access-table]
level: practitioner
status: docs-checked
description: "Build check_client_access, check_sender_access and check_recipient_access tables with OK, REJECT, DISCARD and HOLD actions."
sources:
  - https://www.postfix.org/access.5.html
  - https://www.postfix.org/SMTPD_ACCESS_README.html
  - https://www.postfix.org/postmap.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access maps tables

**Goal:** allow and block by IP, domain or address (access(5) manual).
## Steps
1. `smtpd_client_restrictions = check_client_access hash:/etc/postfix/client_access`
2. Table: `192.0.2.50  REJECT policy` and `example.net  OK`.
3. `postmap /etc/postfix/client_access && postfix reload`.
4. For senders: `check_sender_access hash:/etc/postfix/sender_access` with `bad.example  REJECT`.
## Failure modes
- Trailing text after REJECT is returned to the sender; keep it neutral.
- `OK` only accepts the match inside that restriction list; a REJECT or DEFER result in a list causes the lists after it to be skipped (SMTPD_ACCESS_README).
## Verify
- `postmap -q 192.0.2.50 hash:/etc/postfix/client_access` returns `REJECT policy`.
- A test connection from that address is rejected with `$access_map_reject_code` (default 554).

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): access(5), SMTPD_ACCESS_README, postmap(1), postconf(5).
Confirmed: `check_client_access`, `check_sender_access`, `OK` and `REJECT optional text`, `access_map_reject_code` default 554, `postmap -q`, restriction-list skipping on REJECT.
Corrected or removed: the claim that OK stops only its own list (reworded to what SMTPD_ACCESS_README says), the fixed 554 wording.
Method: documentation only; no commands were run.
