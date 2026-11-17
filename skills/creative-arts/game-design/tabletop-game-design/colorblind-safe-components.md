---
id: creative-arts.game-design.tabletop-game-design.colorblind-safe-components
name: colorblind-safe-components
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, colorblind-components, colour-blindness, accessibility, component-design, iconography]
level: practitioner
status: draft
description: "Make board game components colour-blind safe: redundant shape and icon coding, safe palettes, simulator checks, contrast and testing with colour-blind players."
sources:
  - https://www.color-blindness.com/coblis-color-blindness-simulator/
  - https://jfly.uni-koeln.de/color/
  - https://gameaccessibilityguidelines.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour-blind-safe components

**Goal:** no game information is carried by colour alone. Around 8% of men and 0.5% of
women of Northern European ancestry have some colour vision deficiency, mostly red-green
(deuteranomaly / protanomaly), so at a 4-player table it is common.

## Rules
1. **Redundant coding:** every colour that means something also has a shape, symbol,
   pattern or letter. Player colours: distinct meeple shapes or a symbol on each piece.
   Card suits: an icon in the corner, not just a frame colour.
2. **Avoid problem pairs** as the only distinction: red/green, green/brown, blue/purple,
   light green/yellow, pink/grey.
3. **Use a tested palette:** Okabe and Ito's colour-universal palette (black, orange,
   sky blue, bluish green, yellow, blue, vermillion, reddish purple) stays distinguishable
   under common deficiencies.
4. **Contrast in value:** colours should differ in lightness, not only hue; check by
   converting art to greyscale.
5. **Player aids** and the rulebook use the same symbols as components.

## Check procedure
1. Export every component face to images.
2. Run them through a simulator (Coblis, or Photoshop / Illustrator proof setup
   Colour Blindness - Protanopia and Deuteranopia types).
3. Inspect: can every distinction needed for play still be made? List failures.
4. Test with at least one colour-blind player in physical lighting (warm table lamps
   shift colours).
5. Fix with shapes and icons first; recolouring alone is fragile.

## Common fixes
| Problem | Fix |
|---|---|
| Red/green player cubes | different shapes, or swap green for blue |
| Colour-only resource tokens | unique silhouette per resource |
| Coloured map regions | pattern fills, border icons |
| Card colour suits | suit icon plus colour |

## Gotchas
- Printing shifts colours from screen; check printer proofs, not only files.
- Tiny icons fail as redundancy; size them for table distance.
- Metallic and translucent components read differently under simulation; test physically.

## Verify
- [ ] Every component passes protanopia, deuteranopia and tritanopia simulation.
- [ ] Greyscale version is fully playable.
- [ ] Colour-blind tester completed a game without help.
