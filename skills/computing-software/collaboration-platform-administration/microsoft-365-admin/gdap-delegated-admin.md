---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.gdap-delegated-admin
name: gdap-delegated-admin
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [gdap-delegated-admin]
level: advanced
status: draft
description: Understand granular delegated admin privileges for partner-managed tenants.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Partner delegated access (GDAP)
**Goal:** Understand granular delegated admin privileges for partner-managed tenants.

- GDAP replaced DAP: customer approves a relationship with specific roles and a time limit (max 2 years; confirm).
- Partner assigns security groups to the relationship's roles in Partner Center.
- Customers review in Admin center > Settings > Partner relationships.
- Terminate relationships that are no longer needed.

## Gotchas
- Some roles cannot be delegated via GDAP; check the supported-roles list.
- Expiry silently removes partner access; set renewal reminders.

## Self-check
Partner relationships lists the roles and an end date for every partner.
