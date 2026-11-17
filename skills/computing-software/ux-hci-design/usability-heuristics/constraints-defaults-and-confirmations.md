---
id: computing-software.ux-hci-design.usability-heuristics.constraints-defaults-and-confirmations
name: constraints-defaults-and-confirmations
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [input-constraints, confirmation-dialogs]
level: practitioner
status: draft
description: "Use input constraints, safe defaults and high-cost-only confirmation dialogs to prevent errors."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constraints, defaults, confirmations
- Pickers over free text for dates and enumerations; `type`, `inputmode`, `min`/`max`, `pattern` attributes in HTML.
- Safe defaults: the default option is the least harmful.
- Confirmation dialogs only for rare, high-cost, irreversible actions; overuse trains users to click through.
- For truly dangerous actions, type-to-confirm (enter the resource name).
- Show inline validation hints before submit, not just after.

## Verify
- [ ] Each confirmation dialog protects an irreversible action; others use undo.
