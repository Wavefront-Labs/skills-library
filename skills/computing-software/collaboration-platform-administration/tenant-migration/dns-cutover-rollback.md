---
id: computing-software.collaboration-platform-administration.tenant-migration.dns-cutover-rollback
name: dns-cutover-rollback
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [dns-cutover-rollback, mig-cutover-validation]
level: practitioner
status: draft
description: Execute the MX and autodiscover cutover with a rollback plan.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DNS cutover and rollback
**Goal:** Execute the MX and autodiscover cutover with a rollback plan.

- Lower TTLs 48-72 hours earlier; record original values.
- Change MX, autodiscover CNAME and SPF in a window; notify users.
- Rollback = restore original records; keep source mailboxes intact until sign-off.
- Check mail flow in both directions immediately.

## Gotchas
- Mail sent during propagation can split; keep both systems accepting mail where possible.
- Don't delete the source early.

## Self-check
Test messages route to the new system; `nslookup` returns the new MX.
