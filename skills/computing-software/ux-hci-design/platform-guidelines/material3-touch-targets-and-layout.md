---
id: computing-software.ux-hci-design.platform-guidelines.material3-touch-targets-and-layout
name: material3-touch-targets-and-layout
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [material3-layout, window-size-classes, pg-material]
level: practitioner
status: draft
description: "Use 48 dp touch targets, 8 dp grid spacing and compact/medium/expanded window size classes in Material 3."
sources:
  - https://m3.material.io/foundations/layout/understanding-layout/overview
  - https://m3.material.io/foundations/designing/structure
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Material layout
- Touch targets at least 48 x 48 dp even if the visual is smaller.
- Spacing on a 4/8 dp rhythm.
- Window size classes: compact (under 600 dp), medium (600-839 dp), expanded (840 dp and up) with larger classes added in recent updates; choose navigation bar, rail or drawer accordingly.
- Canonical layouts: list-detail, feed, supporting pane.

## Verify
- [ ] Resize the window in a foldable/tablet emulator; navigation component switches properly.
