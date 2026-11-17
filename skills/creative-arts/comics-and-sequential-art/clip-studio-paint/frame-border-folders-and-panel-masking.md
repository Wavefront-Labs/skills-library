---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.frame-border-folders-and-panel-masking
name: frame-border-folders-and-panel-masking
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-frame-border, csp-frame-folder, layer-masking, breaking-panel-border, bleed-panel, frame-mask]
level: practitioner
status: draft
description: "Use CSP frame border folders to mask art to each panel: drawing inside folders, breaking out of panels, bleed panels to the canvas edge, and organising layers per panel."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://tips.clip-studio.com/en-us
  - https://www.clipstudio.net/en/functions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frame border folders and panel masking

**Goal:** draw freely while each panel's art stays clipped to its border, and break
out deliberately when needed.

## How masking works
- Each frame border folder masks the layers inside it to the panel shape. Draw on
  layers placed inside a panel's folder and anything outside the border is hidden
  (not deleted).
- Clicking a panel with a drawing tool while "Edit target: auto" selects the right
  folder in some versions; otherwise select the folder's layer manually.

## Breaking the border
- Put the breakout element on a layer **outside** the frame folders (above them), or
- Edit the folder's mask: select the frame folder's mask thumbnail and paint to reveal
  extra area (white reveals, transparent hides).

## Bleed panels
- With the Object tool, drag the panel's edge beyond the trim to the bleed line (or
  canvas edge); the mask extends and art bleeds.

## Organisation
```
Text (balloons, captions)
Panel 3 folder: inks / flats / bg
Panel 2 folder: ...
Panel 1 folder: ...
Paper
```
Name folders by panel number. Keep text layers outside panel folders so balloons can
cross gutters.

## Gotchas
- Drawing on a layer outside the folder by mistake: art appears in gutters.
- Rasterising frames too early loses easy editing.

## Verify
- [ ] Art for each panel lives inside its folder; breakouts intentional.
- [ ] Bleed panels reach the bleed line.
