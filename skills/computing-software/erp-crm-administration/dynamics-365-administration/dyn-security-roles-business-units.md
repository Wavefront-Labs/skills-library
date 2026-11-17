---
id: computing-software.erp-crm-administration.dynamics-365-administration.dyn-security-roles-business-units
name: dyn-security-roles-business-units
category: computing-software
field: erp-crm-administration
product: dynamics-365-administration
tags: [dynamics-365-administration, dyn-dataverse-security, dyn-security-roles-business-units]
level: advanced
status: draft
description: "Control record access with roles, depth and business units."
sources: ['https://learn.microsoft.com/en-us/dynamics365/', 'https://learn.microsoft.com/en-us/power-platform/admin/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure security roles and business units
**Goal:** Control record access with roles, depth and business units.

- Privileges are Create, Read, Write, Delete, Append, Append To, Assign, Share; each has an access level (User, Business Unit, Parent: Child Business Units, Organization).
- Users get roles directly or through teams; business units form the hierarchy.
- Use the least privileged role and test with Check Access.

## Gotchas
- Combining roles is additive; there is no deny.

## Self-check
Check Access shows the expected privileges on a record.
