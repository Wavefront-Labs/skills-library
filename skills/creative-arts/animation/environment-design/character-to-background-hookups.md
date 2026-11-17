---
id: creative-arts.animation.environment-design.character-to-background-hookups
name: character-to-background-hookups
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, layout-art, bg-hookup, contact-points, layout, continuity]
level: practitioner
status: draft
description: "Plan character-to-background hookups: contact points with floors, chairs, doors and props drawn in layout so animation and BG register exactly."
sources:
  - https://animationguild.org/
  - https://en.wikipedia.org/wiki/Traditional_animation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character-to-BG hookups and contact points

Goal: characters who actually sit on the chair, lean on the wall and grip the railing in
the background, with no floating or intersection.

## Hookup points to define in layout
- Floor contact line (where feet plant), including steps and slopes.
- Seats, beds, tables: the exact seat height and edge.
- Handles, railings, door knobs: positions the hand registers to.
- Walls and frames characters lean against.
- Props shared between character and BG levels (a cup on the table that gets picked up).

## Method
1. In the layout, draw the character's key poses in position over the BG in a second colour
   (the posing layout).
2. Mark contact points with crosses and labels ("hand reg to knob", "sit line").
3. If a prop changes ownership (on BG, then in hand), split it: BG version until the pick-up
   frame, animation version after. Note the swap frame.
4. Painters keep contact areas clean and in line with the layout; animators register to the marks.
5. For pans/trucks, contact marks move with the BG; indicate positions per key.
6. In 3D, the equivalent is snapping characters to set geometry in layout and locking it.

## Failure modes
- Feet floating above the floor or sinking into it.
- Hand missing the handle by a few pixels after BG paint shifts the edge.
- Prop duplicated (on table and in hand) for a frame at the swap.

## Verify
- [ ] Contact marks on every layout with interaction.
- [ ] Prop swaps noted with frame numbers.
- [ ] Composite check at contact frames.

Related: `creative-arts.animation.environment-design.overlays-and-underlays`,
`creative-arts.animation.principles.prop-handling-animation`.
