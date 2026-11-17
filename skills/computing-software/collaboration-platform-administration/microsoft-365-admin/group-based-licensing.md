---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.group-based-licensing
name: group-based-licensing
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [group-based-licensing]
level: practitioner
status: draft
description: Assign licences to a security group so membership drives entitlements.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Group-based licensing
**Goal:** Assign licences to a security group so membership drives entitlements.

- Entra/Admin center > Billing > Licenses > select product > Licenses > Assign to a group (group-based licensing needs Entra ID P1 or an equivalent licence; confirm in current docs).
- Use dynamic groups for rule-based membership, e.g. `user.department -eq "Sales"`.
- Disable specific service plans per assignment to turn off unneeded features.
- Review the group's Licenses blade for processing errors.

## Gotchas
- Conflicting service plans or insufficient licences leave users in an error state; fix and reprocess.
- Removing a user from the group removes the licence, and with it mailbox/OneDrive data eventually.

## Self-check
The group's licence blade shows 0 users with errors and each member shows the licence.
