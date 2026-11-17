---
id: computing-software.ux-hci-design.usability-heuristics.personalisation-and-adaptive-defaults
name: personalisation-and-adaptive-defaults
category: computing-software
field: ux-hci-design
product: usability-heuristics
tags: [adaptive-defaults, personalisation-ux]
level: practitioner
status: draft
description: "Remember preferences and recent choices, but keep the interface predictable and let users override."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Personalisation
- Remember last-used settings (sort order, filters, layout) per user.
- Predictive suggestions need an obvious way to ignore or reset.
- Avoid moving core controls based on usage; unstable positions break muscle memory.
- Respect OS-level preferences via media queries: `prefers-color-scheme`, `prefers-reduced-motion`, `prefers-contrast`.

## Verify
- [ ] Reset-to-default exists and works for every remembered preference.
