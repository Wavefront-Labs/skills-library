---
id: creative-arts.graphic-design.adobe-illustrator.repeat-radial-grid-mirror
name: repeat-radial-grid-mirror
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, ai-patterns, repeat-radial, repeat-mirror, repeat-grid, symmetry]
level: intro
status: draft
description: "Use Illustrator Repeat (Radial, Grid, Mirror) for live symmetric artwork: instance counts, radius, editing the source, and expanding for output."
sources:
  - https://helpx.adobe.com/illustrator/using/repeat-objects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Repeat: radial, grid and mirror

**Goal:** live repeated artwork that updates when you edit the source shape.

## Create
Select art, Object > Repeat > **Radial**, **Grid** or **Mirror** (or the Properties panel Quick Actions).
- **Radial**: number of instances, radius; drag the circle handles; Reverse Overlap. For
  mandalas, clock faces, flowers, logos built from rotated petals.
- **Grid**: horizontal/vertical spacing handles; grid type (Grid, Brick by Row/Column);
  flip rows/columns - wallpaper and backgrounds.
- **Mirror**: drag/rotate the axis line - draw one half of a symmetric logo/character.

## Editing
- Double-click into the repeat (Isolation mode) and edit the source - all instances update.
- Add new shapes inside isolation mode to include them in the repeat.
- Repeat Options (Object > Repeat > Options) for precise values.

## Output
- Object > **Expand** converts to normal grouped artwork. Do this before handoff to older
  Illustrator versions or other apps and for SVG/print cleanup.
- Combine with Pathfinder/Shape Builder only after expanding.

## Gotchas
- Mirror axis snapping can drift; set the axis angle in Options for exact symmetry.
- Radial repeats of text are not editable as text per instance.

## Verify
- [ ] Expanded copy matches the live repeat; source kept in a hidden layer for edits.
