---
id: creative-arts.graphic-design.adobe-illustrator.global-swatches-and-color-groups
name: global-swatches-and-color-groups
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, global-swatches, color-groups, swatch-library, tints, select-same-fill, brand-colours, ase]
level: practitioner
status: draft
description: "Build Illustrator colour with global swatches and colour groups so one swatch edit recolours every object and tint, and share palettes as libraries or ASE files."
sources:
  - https://helpx.adobe.com/illustrator/using/using-creating-swatches.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Global swatches and colour groups

**Goal:** change a brand colour once and have every use, including tints, update.

## Make swatches global
- Swatches panel > New Swatch (or drag a fill colour into the panel). Tick **Global**.
- A global swatch shows a white corner triangle in the panel.
- Objects filled with a global swatch stay linked: double-click the swatch, edit values,
  every object updates. **Tints** of a global swatch (Color panel tint slider) keep the
  link and update too.
- Non-global (plain process) swatches only apply values once; editing the swatch changes
  nothing already painted.
- Spot colours are always global (see the spot colours skill).

## Colour groups
- Select swatches > New Color Group (folder icon). Name them by role: `Brand primary`,
  `Neutrals`, `Chart palette`.
- Groups are what Recolor Artwork and Color Guide work with, and what you export.

## Convert a messy file to global swatches
1. Select All, Swatches panel menu > **Add Selected Colors** - creates swatches from
   every colour in use (tick Global in the dialog).
2. Or select an object, **Select > Same > Fill Color**, then assign the global swatch.
3. Delete unused: panel menu > Select All Unused > delete.

## Share
- **CC Libraries:** drag the group into a library; teammates and InDesign/Photoshop get it.
- **ASE file:** panel menu > Save Swatch Library as ASE (for exchange with other apps), or
  as AI for Illustrator-only (keeps groups and spot definitions).
- Open others: Swatch Libraries menu > Other Library.

## Gotchas
- Colours defined inside a gradient are linked only if the gradient stops use global swatches.
- Pasting art from another file with same-named swatches but different values triggers a
  "Swatch Conflict" dialog - choose Merge only if values really match.
- Record values in brand guidelines from the swatch (CMYK, RGB, HEX), not by eyedropper on screen.

## Verify
- [ ] Every brand colour exists as a named global swatch in a named group.
- [ ] Editing a swatch recolours all instances including tints.
- [ ] Unused swatches removed before handoff.
