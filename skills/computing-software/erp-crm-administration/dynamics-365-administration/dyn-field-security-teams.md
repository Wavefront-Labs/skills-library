---
id: computing-software.erp-crm-administration.dynamics-365-administration.dyn-field-security-teams
name: dyn-field-security-teams
category: computing-software
field: erp-crm-administration
product: dynamics-365-administration
tags: [dynamics-365-administration, dyn-field-security-teams]
level: advanced
status: draft
description: "Protect individual columns and share via teams."
sources: ['https://learn.microsoft.com/en-us/dynamics365/', 'https://learn.microsoft.com/en-us/power-platform/admin/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use field security profiles and teams
**Goal:** Protect individual columns and share via teams.

- Enable column security and add users or teams to a field security profile with Read/Update/Create permissions.
- Owner teams, access teams and Microsoft Entra group teams grant roles and share records.
- Audit sharing.

## Gotchas
- Secured columns hide values from users not in the profile, including in API results.

## Self-check
Non-member sees the column masked.
