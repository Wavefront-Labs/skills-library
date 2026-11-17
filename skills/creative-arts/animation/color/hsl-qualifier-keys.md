---
id: creative-arts.animation.color.hsl-qualifier-keys
name: hsl-qualifier-keys
category: creative-arts
field: animation
product: color
tags: [hsl-qualifier, secondary-grading, qualifier, key, matte-finesse, davinci-resolve, skin-tone, colour-isolation, grading]
level: practitioner
status: draft
description: "Isolate a colour range with HSL qualifiers in DaVinci Resolve for secondary grades: picking, refining ranges, matte finesse, and why keys are easier on flat animation."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.blackmagicdesign.com/products/davinciresolve/training
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HSL qualifier keys

**Goal:** change one colour (a character's jacket, a sky, a glowing sign) without touching the
rest. A qualifier builds a matte from hue, saturation and luminance ranges.

## Procedure (Resolve Colour page)

1. Add a **serial node** after your primaries (secondary nodes come after balance).
2. Qualifier palette, HSL mode. Pick with the eyedropper on the target; drag across the area to
   include its range.
3. Turn on **Highlight** (Shift+H) to see the matte over grey.
4. Refine each range: hue width and softness first (most selective), then saturation (drop low-sat
   greys), then luminance (exclude shadows/highlights).
5. **Matte Finesse**: Clean Black / Clean White to remove speckle, Blur Radius 1-5 for soft edges,
   Denoise for noisy renders, In/Out ratio to shrink/grow.
6. Grade inside the node: hue rotation, saturation, gain.
7. Combine with a window to limit area (`creative-arts.animation.color.power-windows`), connected
   via the node's key input or simply by adding a window on the same node.

## Animation advantages and traps

- Flat colour styles key almost perfectly: a palette colour is one tight hue range. Use narrow
  hue ranges and tiny softness.
- Same hue reused elsewhere (shared palette across characters/props) leaks into the key; add a
  window or tracked window.
- Gradient shading/rim lights change saturation and luma across the object; widen sat/lum, not hue.
- Line art antialiasing produces edge pixels of mixed colour; a slight blur in matte finesse
  avoids a hard keyed outline.

## Alternatives

- 3D qualifier (keys in a colour volume) for difficult mixed hues.
- Render-side IDs (cryptomatte/object IDs) delivered as mattes: perfect isolation for CG shows;
  bring them in as external mattes rather than keying.

## Verify

Highlight view on the first, middle and last frame: the matte is solid on the target, clean
elsewhere, and does not chatter frame to frame on playback.
