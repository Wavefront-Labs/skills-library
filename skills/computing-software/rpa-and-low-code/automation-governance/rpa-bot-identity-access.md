---
id: computing-software.rpa-and-low-code.automation-governance.rpa-bot-identity-access
name: rpa-bot-identity-access
category: computing-software
field: rpa-and-low-code
product: automation-governance
tags: [automation-governance, rpa-governance-coe, rpa-bot-identity-access]
level: advanced
status: draft
description: "Treat bots as privileged non-human identities."
sources: ['https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit', 'https://docs.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manage bot identities and access
**Goal:** Treat bots as privileged non-human identities.

- One account per bot and environment, least privilege, no interactive admin rights, MFA exceptions documented and compensating controls.
- Store credentials in a vault; rotate; review monthly.
- Log all bot actions for audit.

## Gotchas
- Bots with shared accounts hide accountability.

## Self-check
Access review lists each bot identity and owner.
