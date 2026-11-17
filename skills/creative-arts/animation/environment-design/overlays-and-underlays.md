---
id: creative-arts.animation.environment-design.overlays-and-underlays
name: overlays-and-underlays
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, layout-art, overlay-underlay, background-layers, compositing, hookup]
level: practitioner
status: draft
description: "Split backgrounds into overlays and underlays: elements in front of characters on separate levels, clean cut lines, and how they compose over animation."
sources:
  - https://animationguild.org/
  - https://en.wikipedia.org/wiki/Traditional_animation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overlays and underlays

Goal: backgrounds broken into levels so characters can pass behind foreground objects
(overlays, OL) and over background elements that need separate handling (underlays, UL).

## Definitions
- **Overlay (OL)**: a BG element painted on its own level and composited above the
  character (a tree trunk, a table edge, a door frame the character walks behind).
- **Underlay (UL)**: an element under the characters but separate from the main BG,
  usually because it moves, is reused, or needs a different camera move/parallax.
- **Held cel / hookup level**: a static part of a character or prop painted to match the BG.

## Method
1. In the layout, mark every place a character goes behind something. Each is an OL.
2. Draw the cut line on the layout where the OL separates from the BG; it should follow
   a natural edge (trunk outline, counter edge), never cut through open space.
3. Label levels: BG, UL1, OL1, OL2 with their stacking order relative to character levels (A, B, C).
4. Painters paint the OL with clean alpha edges and a little overlap under the cut so no
   gap appears in comp.
5. Match lighting/colour across the cut; OL and BG are painted together then split.
6. Note any OL that moves (parallax, wind) for compositing.

## Failure modes
- Character feet or hands disappearing into a painted-in BG with no OL.
- Cut lines through soft gradients, leaving visible seams.
- Wrong stacking order between OL and character levels.

## Verify
- [ ] Every behind-object moment has an OL.
- [ ] Cut lines follow edges.
- [ ] Level stacking documented on the layout.

Related: `creative-arts.animation.environment-design.character-to-background-hookups`,
`creative-arts.animation.environment-design.multiplane-and-parallax-layers`.
