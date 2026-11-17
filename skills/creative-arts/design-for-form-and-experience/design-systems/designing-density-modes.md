---
id: creative-arts.design-for-form-and-experience.design-systems.designing-density-modes
name: designing-density-modes
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [density-modes, density, compact-mode, comfortable-mode, ui-density, design-tokens, data-ui]
level: practitioner
status: draft
description: "Design density modes (compact, default, comfortable) as token sets: adjust spacing, row height, type and icon size together, keeping touch targets and accessibility intact."
sources:
  - "Material Design - Applying density (m2.material.io/design/layout/applying-density.html)"
  - "Carbon Design System - Data table row heights (carbondesignsystem.com/components/data-table/usage)"
  - "Atlassian Design System - Spacing and compact density (atlassian.design)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Density modes

**Goal:** let power users see more per screen and casual users get breathing room, without maintaining forks of the UI.

## What changes
- **Vertical padding and row height** (list rows 48 default, 40 compact, 56 comfortable; Material density uses steps of 4 dp: 0, -1, -2, -3 reducing control height by 4 dp each; min control height in compact about 32 px for pointer UIs).
- **Gaps** between controls and sections shift one spacing step.
- **Icon sizes** (24 default, 20 compact) and sometimes type (14 vs 13).
- What does **not** change: font size minimums for readability, colour contrast, focus rings, hit areas on touch.

## Implementation
1. Define **tokens per density** (`density.control.height`, `density.row.height`, `density.padding.inline`) in a mode collection (Figma variable modes Compact/Default/Comfortable) and in CSS via a data attribute: `[data-density="compact"] { --row-height: 36px; --pad-y: 4px; }`.
2. Build components against density tokens only; avoid pixel literals.
3. Use hit-area padding so compact controls remain at least 24x24 CSS px (WCAG 2.2) and 44-48 on touch; **disable compact on coarse pointers** (`@media (pointer: coarse)`).
4. Provide the user setting (account preference, table toolbar) and persist per user and per view; default by product type (admin tools compact, consumer comfortable).
5. Test the longest content, localisation and zoom at 200 percent.

## Gotchas
- Compacting only paddings but not row heights yields uneven layouts.
- Dense mode must not drop information; use progressive disclosure instead of tiny text.

## Verify
- [ ] Density is tokenised and switchable without code forks.
- [ ] Targets and text sizes meet minimums in compact mode.
- [ ] User choice persisted; touch devices constrained.
