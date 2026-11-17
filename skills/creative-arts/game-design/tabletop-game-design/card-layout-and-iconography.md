---
id: creative-arts.game-design.tabletop-game-design.card-layout-and-iconography
name: card-layout-and-iconography
category: creative-arts
field: game-design
product: tabletop-game-design
tags: [game-design, tabletop-game-design, card-layout, iconography, component-design, graphic-design, bleed, safe-zone, readability, card-templates]
level: practitioner
status: draft
description: "Lay out playing cards for play: information hierarchy, corner indices for fanned hands, icon systems, text size, bleed and safe zones, and readability tests across the table."
sources:
  - https://www.thegamecrafter.com/help/templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Card layout and iconography

**Goal:** cards that players can read quickly in hand, on the table and upside down, with
a consistent icon language.

## Information hierarchy
1. **What do players need when the card is in a fanned hand?** Put it in the top-left
   corner (cost, suit, number) - fanned cards show only that corner.
2. **What do players need from across the table?** Large, high-contrast elements (type
   colour, big icon).
3. **What is read once?** Rules text, flavour text: smaller, lower on the card.

## Icon system
- One icon = one meaning; build a legend.
- Icons with **text fallback** for complex effects early; condense to icons once learned.
- Shapes distinguishable without colour (colour-blind players).
- Keep icon vocabulary small; dozens of icons become a language to learn.

## Print specs (check your printer's templates)
| Spec | Typical value |
|---|---|
| Poker card | 63.5 x 88.9 mm (2.5 x 3.5 in) |
| Bridge card | 57 x 89 mm |
| Bleed | ~3 mm (1/8 in) beyond trim |
| Safe zone | keep text ~3 mm or more inside trim |
| Resolution | 300 dpi at final size |
Printers (The Game Crafter, MPC, Panda, etc.) publish their own templates; use them.

## Procedure
1. Sketch the template with zones; test it with real data via a data merge (see
   `creative-arts.game-design.tabletop-game-design.nandeck-card-generation`).
2. Print at actual size; test in a fanned hand, at arm's length, and from across the
   table, under typical room light.
3. Check the longest rules text card fits at the minimum font size (commonly ~7-8 pt
   minimum for body text; test with players).
4. Colour-blind simulation (e.g. Color Oracle) on the final palette.

## Gotchas
- Screen previews hide readability problems; always print.
- Upside-down readability matters for shared tableau cards; consider duplicate
  indices.
- Text-heavy cards slow play and complicate localisation.

## Verify
- [ ] Corner indices readable in a fanned hand.
- [ ] Icon legend complete; icons distinguishable in greyscale.
- [ ] Printed proofs tested at table distance.
- [ ] Bleed/safe zones match the printer's template.
