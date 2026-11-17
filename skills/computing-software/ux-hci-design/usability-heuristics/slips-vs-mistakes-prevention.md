---
id: computing-software.ux-hci-design.usability-heuristics.slips-vs-mistakes-prevention
name: slips-vs-mistakes-prevention
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [slips-and-mistakes, error-types, uh-error-prevention]
level: practitioner
status: draft
description: "Prevent slips with constraints and defaults, and mistakes with clear models, previews and confirmation where cost is high."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slips versus mistakes
- **Slip**: right goal, wrong execution (typo, mis-click, adjacent buttons). Reduce with constraints, input masks, larger spacing, undo, sensible defaults.
- **Mistake**: wrong goal or model (misunderstanding). Reduce with clear labels, previews, examples, and good information architecture.
- **Capture slips**: a habitual action overrides the intended one; change the habit path (different confirm text).

## Tactics
- Disable or hide impossible actions, but explain why if disabled.
- Confirm destructive actions by naming what will be lost ("Delete 12 files") rather than "Are you sure?".
- Separate destructive and constructive buttons visually.

## Verify
- [ ] Usability test log shows no repeated error at the same control.
