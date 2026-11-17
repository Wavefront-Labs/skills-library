---
id: computing-software.systems-network-administration.pki-tls-administration.cabf-lifetime-schedule
name: cabf-lifetime-schedule
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cabf-lifetime-schedule, pki-cabf, pki, 47-day, lifetimes, ballot-sc-081, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Plan for the CA/B Forum Baseline Requirements schedule that cuts public TLS certificate validity and domain validation reuse down to 47 and 10 days."
sources:
  - https://cabforum.org/working-groups/server/baseline-requirements/documents/
  - https://raw.githubusercontent.com/cabforum/servercert/main/docs/BR.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate lifetime reduction schedule
Goal: be fully automated before manual renewal becomes impossible.

Baseline Requirements section 6.3.2 (maximum Subscriber Certificate validity) and section 4.2.1 (Domain Name and IP Address validation data reuse), as adopted by ballot SC081 (BR version 2.1.5, adopted 2025-04-11 per the BR change history). Confirm against the current BR text before relying on it.

| Certificate issued | Max validity | Domain/IP validation reuse |
|---|---|---|
| before 2026-03-15 | 398 days | 398 days |
| 2026-03-15 up to 2027-03-15 | 200 days | 200 days |
| 2027-03-15 up to 2029-03-15 | 100 days | 100 days |
| on or after 2029-03-15 | 47 days | 10 days |

- The BR also states a "SHOULD NOT" one day below each maximum (199, 99 and 46 days for the last three rows, 397 before 2026-03-15).
- Subject Identity Information validation reuse is a separate table: 825 days before 2026-03-15, then 398 days from that date.
- The same schedule lists other dated changes, for example certain domain validation methods may not be relied on from 2027-03-15 (3.2.2.4.16, 3.2.2.4.17, 3.2.2.5.2, 3.2.2.5.5) and from 2028-03-15 (3.2.2.4.4, 3.2.2.4.13, 3.2.2.4.14). Check which method your CA or ACME client uses.

Planning steps (practice, not BR text):
1. Inventory every public certificate and how it is renewed.
2. Move to ACME or the CA's API, and renew well before expiry rather than at the end of validity.
3. Remove human steps: approval emails, ticket-driven CSRs, certificates pinned in appliances without an API.
4. Alert on failed renewals long before expiry, not at expiry.
Gotcha: devices that only import certificates manually (old load balancers, printers) need a terminating proxy or replacement; budget for that before the 100-day step in 2027.

Verify:
- [ ] Every public certificate has an automated renewal job with a tested failure alert.
- [ ] Dry-run renewals succeed under the shortest validity you expect to face.

## Checked
Checked against the CA/B Forum Baseline Requirements source (docs/BR.md on the servercert repository: implementation-date table, 4.2.1 reuse tables, 6.3.2 validity text, change history) and the BR documents index page.
Removed: the cited ballot post URL (returns 404), the "renew at 2/3 of lifetime, about day 31" figure and the "47-day test CA profile" check (not in the BR).
Method: docs-only read of cited pages, 2026-11-08
