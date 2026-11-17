---
id: computing-software.email-administration.mail-server-administration.mx-cutover-plan
name: mx-cutover-plan
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mx-cutover-plan, mx-cutover, cutover-plan, dns-ttl]
level: practitioner
status: draft
description: "Plan the MX cutover: lower TTLs, parallel run, secondary acceptance, final sync and rollback."
sources:
  - https://doc.dovecot.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mx cutover plan

**Goal:** no lost mail during the switch.
## Steps
1. Lower MX TTL to a few minutes at least a day before.
2. Bring up the new server accepting mail for all recipients.
3. Change MX; keep the old server forwarding or holding for several days (senders cache).
4. Run a final imapsync/dsync pass, then lower DNS and decommission.
5. Update PTR, SPF and DKIM for the new IP before cutover.
## Failure modes
- Forgetting SPF includes the new IP: outbound mail from the new host fails SPF.
## Verify
- Send test mail from several providers; confirm arrival on the new host only.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
