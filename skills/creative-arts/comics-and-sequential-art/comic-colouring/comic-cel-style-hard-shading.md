---
id: creative-arts.comics-and-sequential-art.comic-colouring.comic-cel-style-hard-shading
name: comic-cel-style-hard-shading
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, colour-rendering, comic-rendering, comic-cel-shading, hard-shading, multiply-shadows, two-tone-shading]
level: practitioner
status: draft
description: "Render comics with hard-edged cel shading: one shadow and one highlight tone per region, Multiply shadow layers with a consistent shadow colour, and shape design of shadows."
sources:
  - https://en.wikipedia.org/wiki/Cel_shading
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://helpx.adobe.com/photoshop/using/blending-modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cel-style hard shading

**Goal:** clean, graphic rendering that's fast, consistent and reads well at small
sizes.

## Structure
- Flats = base colours.
- **One shadow tone** per region, hard-edged.
- Optional **one highlight** tone, hard-edged.
- Optional second, darker shadow for occlusion (under chin, deep folds).

## Fast technique: shared Multiply shadow layer
1. Layer above FLATS set to **Multiply**.
2. Paint shadows with a single colour (a desaturated cool purple/blue at ~20-35%
   value darkening is common; pure grey makes colours muddy).
3. Use selections from flats or a clipping mask so shadows stay inside forms.
4. Adjust the shadow colour globally afterwards (hue shifts per scene: warm sunset
   vs cool night).
5. Highlights on a **Screen**, **Add (Glow)** or Normal layer with lighter colour.

## Designing shadow shapes
- Follow form: the terminator (light-to-shadow edge) wraps around volumes.
- Respect the inker's blacks and light direction; don't contradict them.
- Simplify: big, clean shapes beat lots of fiddly patches.
- Cast shadows (from one object onto another) give grounding; include them.

## Gotchas
- Shadow on every fold: noisy. Choose major planes.
- Using black or grey Multiply: dulls saturated colours. Tint the shadow.
- Inconsistent light direction between panels.

## Verify
- [ ] One light direction per scene, consistent across panels.
- [ ] Shadow colour tinted and consistent.
- [ ] Shapes clean at print size.
