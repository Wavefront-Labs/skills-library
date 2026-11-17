---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.compliance-boundaries-rbac
name: compliance-boundaries-rbac
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [compliance-boundaries-rbac]
level: advanced
status: draft
description: Delegate Purview with role groups and scope with boundaries.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Purview roles and compliance boundaries
**Goal:** Delegate Purview with role groups and scope with boundaries.

- Roles & scopes > Permissions: role groups such as eDiscovery Manager, Compliance Administrator.
- Compliance boundaries and administrative units restrict users' data scope.
- Audit role group membership.
- Use PIM for just-in-time elevation (reference Entra).

## Gotchas
- Compliance Administrator is powerful; limit it.
- Boundaries apply to eDiscovery; not every solution.

## Self-check
Role group membership export matches the approved list.
