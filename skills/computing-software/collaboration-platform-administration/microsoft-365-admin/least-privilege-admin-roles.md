---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.least-privilege-admin-roles
name: least-privilege-admin-roles
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [least-privilege-admin-roles, m365-admin-roles]
level: practitioner
status: draft
description: Assign the narrowest built-in admin role per task instead of Global Administrator.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Least-privilege admin roles
**Goal:** Assign the narrowest built-in admin role per task instead of Global Administrator.

- Admin center > Roles > Role assignments; or Entra roles (reference, covered by Entra products).
- Common roles: User Administrator, Exchange Administrator, SharePoint Administrator, Teams Administrator, Helpdesk Administrator, Billing Administrator.
- Keep Global Administrator to a few (commonly 2-4) accounts, plus 2 emergency access accounts excluded from Conditional Access.
- Use separate cloud-only admin accounts without mailboxes or licences beyond what's needed.
- Review assignments quarterly.

## Gotchas
- Privileged Identity Management is an Entra feature; use it for just-in-time elevation where licensed.
- Global Reader is read-only but sees everything; still audit it.

## Self-check
List role members (`Get-MgDirectoryRole`/admin center) and confirm each has a documented reason.
