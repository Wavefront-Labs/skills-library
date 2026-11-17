---
id: computing-software.collaboration-platform-administration.google-workspace-admin.org-units-inheritance
name: org-units-inheritance
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [org-units-inheritance, gws-org-structure]
level: practitioner
status: draft
description: Design OUs and understand how settings inherit and override.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Organizational units and settings inheritance
**Goal:** Design OUs and understand how settings inherit and override.

- Admin console > Directory > Organizational units; child OUs inherit parent settings until overridden.
- Use OUs for differing service settings (for example contractors, students); use groups for access.
- Move users via the console or GAM/API; changes can take up to 24 hours to propagate.
- Keep structure shallow (2-3 levels).

## Gotchas
- A user belongs to exactly one OU; groups can apply some settings through access groups or group-based settings (service-dependent).
- Overriding a setting at a child OU breaks later parent updates for it.

## Self-check
Open a user and use 'Show effective settings' style views (or Admin console > Reporting) to confirm the setting source.
