---
id: computing-software.ux-hci-design.interaction-design.fitts-law-target-design
name: fitts-law-target-design
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [fitts-law, target-acquisition, id-laws-of-ux]
level: practitioner
status: draft
description: "Size and position targets using Fitts's law: time grows with distance and shrinks with target width."
sources:
  - https://lawsofux.com/fittss-law/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fitts's law
MT = a + b * log2(D/W + 1) (Shannon formulation; D distance to target, W width along the movement axis).
Implications:
- Make frequent and important targets large and near.
- Screen edges and corners are effectively infinite targets for mouse (menu bars at the edge).
- Increase hit area with padding beyond the visible shape.
- Separate destructive buttons from frequent ones.
- Touch: minimum sizes in guidelines (WCAG 24 CSS px; Apple 44 pt; Material 48 dp).

## Verify
- [ ] Primary actions on mobile sit in thumb-reachable zones and meet minimum size.
