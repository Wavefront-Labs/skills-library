---
id: computing-software.email-administration.mail-server-administration.restore-testing
name: restore-testing
category: computing-software
field: email-administration
product: mail-server-administration
tags: [restore-testing, disaster-recovery]
level: practitioner
status: draft
description: "Test restores of a mailbox and of the whole server regularly, including DKIM keys and DNS cutover steps."
sources:
  - https://doc.dovecot.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restore testing

**Goal:** prove you can recover within the time you promised.
## Steps
1. Restore one user's mailbox into a scratch Dovecot instance; check message counts and flags.
2. Rebuild a server from config and keys on a scratch host; use `postfix check` and `doveconf -n`.
3. Time the exercise and write the runbook, including DNS TTLs and PTR requirements for new IPs.
## Failure modes
- Lost DKIM private key forces a new selector and delays.
## Verify
- A written restore time and a mailbox that opens correctly in a client.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
