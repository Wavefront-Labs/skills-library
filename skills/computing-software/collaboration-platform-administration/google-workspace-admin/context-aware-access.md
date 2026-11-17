---
id: computing-software.collaboration-platform-administration.google-workspace-admin.context-aware-access
name: context-aware-access
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [context-aware-access]
level: advanced
status: draft
description: Restrict apps based on device, IP and location.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Context-Aware Access
**Goal:** Restrict apps based on device, IP and location.

- Security > Access and data control > Context-Aware Access (edition-dependent, confirm).
- Create access levels (device policy, IP subnet, geo) and assign to apps and OUs/groups.
- Use endpoint verification to report device attributes.
- Test with a pilot OU; use 'Monitor only' where offered.

## Gotchas
- Misconfigured levels lock out admins; exclude a break-glass admin.
- Mobile app access follows device policy support; verify.

## Self-check
Blocked scenario shows the access denied page for a test user.
