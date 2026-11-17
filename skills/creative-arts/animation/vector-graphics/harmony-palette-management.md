---
id: creative-arts.animation.vector-graphics.harmony-palette-management
name: harmony-palette-management
category: creative-arts
field: animation
product: vector-graphics
tags: [palette-management, ink-and-paint, toon-boom, harmony, colour-palettes, master-palette, palette-list, colour-models, palette-override, scene-palette, palette-styling]
level: practitioner
status: draft
description: "Manage colour palettes in Toon Boom Harmony: master vs scene/element palettes, palette lists, linking colour IDs so global colour changes repaint every drawing."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Harmony palette management

**Goal:** colour defined once per character/prop and referenced by every drawing, so a colour change (or a night
version) updates the whole series without repainting.

## How Harmony colour works

Painted areas store a **colour ID**, not a colour value. The palette maps IDs to values. Change the swatch, every
area using that ID updates in every drawing using that palette.

## Palette scopes

| Scope | Use |
|---|---|
| Environment/job (master) palettes | character and prop palettes shared across all scenes of a production (database setups) |
| Scene palettes | scene-specific colours |
| Element palettes | per drawing element (rare; avoid for shared characters) |
The **palette list** order determines which palette wins when the same colour is referenced; keep master character
palettes in the shared location and imported into scenes, not copied.

## Production practice

- One palette per character (`MIA.plt`) with named swatches (`MIA_skin`, `MIA_skin_shadow`, `MIA_hair`,
  `MIA_line`), matching the colour model sheet.
- Line colours in the same palette (so line colour styling also updates).
- Day/night/mood versions: palette **styling** via cloned palettes (same IDs, different values) swapped per scene,
  not repainting (Harmony "clone palette" / palette styles).

## Gotchas

- Copying drawings between scenes with **local** palette copies creates duplicates with new IDs: later master
  changes don't propagate. Import/link the master palette.
- Deleting a swatch in use turns areas red (missing colour); check usage first.
- Raster/bitmap layers in Harmony don't use palette IDs for colour; keep paint on vector layers.

## Verify

Change one master swatch temporarily: every scene using the character updates; scenes still showing the old colour
are using a local copy and need relinking.
