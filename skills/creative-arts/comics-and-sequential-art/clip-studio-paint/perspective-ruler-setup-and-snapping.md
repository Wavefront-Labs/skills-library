---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.perspective-ruler-setup-and-snapping
name: perspective-ruler-setup-and-snapping
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-rulers, csp-perspective-ruler, csp-snap-to-ruler, vanishing-points, eye-level, snap-to-special-ruler, perspective]
level: practitioner
status: draft
description: "Set up CSP perspective rulers: 1/2/3-point creation, placing vanishing points and eye level, sharing rulers across layers, toggling snapping, and matching rulers to 3D or photo reference."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://tips.clip-studio.com/en-us
  - https://en.wikipedia.org/wiki/Perspective_(graphical)
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Perspective ruler setup and snapping

**Goal:** draw backgrounds whose lines snap to correct vanishing points, quickly.

## Create
- Ruler tool > **Perspective ruler**: choose the type (1-point, 2-point, 3-point) in
  Tool property, then drag guide lines on the canvas; each pair of drags defines a
  vanishing point. Or Layer > Ruler/Frame > Create perspective ruler with a type.
- The ruler attaches to the active layer (ruler icon in the Layer palette).

## Adjust
- With the Object tool, drag vanishing points (including off-canvas ones; zoom out),
  the **eye level** line (horizon), and guide lines.
- Fix eye level to keep the horizon horizontal while moving VPs (Object tool property).
- Add or delete vanishing points via the Object tool property or right-click menu.

## Sharing across layers
In the ruler's settings (Object tool or Layer palette ruler icon), choose **Show in
all layers** or **Show in same folder** so inks, flats and pencils all use it.
Alternatively copy the ruler to other layers.

## Snapping
- View > **Snap to special ruler** toggles snapping (also on the command bar).
- With snapping on, strokes snap to whichever VP direction they start closest to;
  draw short test strokes to see which direction it picks.
- Hold the snap toggle off to draw organic elements (plants, people) on the same layer.

## Matching reference
Place the 3D model or photo, then align the ruler's guide lines over its edges; or use
3D layers with "Create perspective ruler" from the 3D camera where available.

## Verify
- [ ] VPs and eye level placed per the panel's camera.
- [ ] Ruler visible on every drawing layer that needs it.
- [ ] Snap toggled off for freehand elements.
