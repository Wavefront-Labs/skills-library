---
id: creative-arts.animation.visual-development.local-color-vs-light-color
name: local-color-vs-light-color
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, color-theory, local-color, light-color, color-constancy, lighting]
level: practitioner
status: draft
description: "Separate local colour from light colour: render an object's own colour as modified by the light's colour, shadows and atmosphere, and keep it identifiable."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Color_constancy
  - https://books.google.com/books?vid=ISBN9781933492964
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local color vs light color

Goal: objects that keep their identity (a red ball is red) while showing the colour of the
light falling on them.

## Concepts (Gurney)
- **Local colour**: the surface's inherent colour under white light.
- **Light colour**: the colour of the illumination (warm sun, blue sky, orange fire).
- Perceived colour = local colour x light colour, plus reflected light and atmosphere.
- **Colour constancy**: the brain corrects for light colour, so painters must paint the actual
  shifted colour while the viewer still reads the local colour.

## Practical effects
- Under orange firelight, blue objects go grey-dark; under sodium light, colour nearly disappears.
- In shadow, local colour shows through the fill colour (red shirt in blue shadow = dark violet-red).
- With distance, local colour fades toward the atmosphere colour.
- Highlights take the light's colour, not the local colour (except metals).

## Method
1. Define each object's local colour in neutral light (the colour model).
2. Define the scene's light colours (key, fill).
3. Multiply: tint the lit side by the key colour, the shadow side by the fill.
4. Check identity: can viewers still name the object's colour?
5. For lighting variant palettes, keep this logic consistent across characters.

## Failure modes
- Local colour pasted unchanged into every lighting condition - looks pasted-on.
- Light colour so strong that character identity is lost.
- Shadows painted as local colour plus black.

## Verify
- [ ] Lit and shadow sides tinted by their light sources.
- [ ] Objects remain identifiable.
- [ ] Variant palettes follow the same logic.

Related: `creative-arts.animation.character-design.model-sheet-turnaround`,
`creative-arts.animation.visual-development.warm-and-cool-contrast`.
