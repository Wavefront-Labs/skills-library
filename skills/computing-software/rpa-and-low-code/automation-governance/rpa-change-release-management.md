---
id: computing-software.rpa-and-low-code.automation-governance.rpa-change-release-management
name: rpa-change-release-management
category: computing-software
field: rpa-and-low-code
product: automation-governance
tags: [automation-governance, rpa-change-release-management]
level: advanced
status: draft
description: "Promote automations through environments with approvals."
sources: ['https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit', 'https://docs.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control changes and releases
**Goal:** Promote automations through environments with approvals.

- Separate dev, test and production; require code review, test evidence and change tickets for production publishes.
- Version packages and keep rollback ready.
- Maintain an inventory with owners.

## Gotchas
- Hot-fixing in production without records breaks audits.

## Self-check
Each production version maps to a change record.
