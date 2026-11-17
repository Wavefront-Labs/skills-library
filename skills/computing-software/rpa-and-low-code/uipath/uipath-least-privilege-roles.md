---
id: computing-software.rpa-and-low-code.uipath.uipath-least-privilege-roles
name: uipath-least-privilege-roles
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-bot-security, uipath-least-privilege-roles]
level: advanced
status: draft
description: "Limit what users and robots can do."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Apply least privilege in Orchestrator
**Goal:** Limit what users and robots can do.

- Use folder-level roles, separate robot accounts per environment, and restrict Edit permissions in production folders.
- Review role assignments periodically.
- Use SSO and MFA for users.

## Gotchas
- Shared robot accounts hide who did what.

## Self-check
Access review lists users per folder and role.
