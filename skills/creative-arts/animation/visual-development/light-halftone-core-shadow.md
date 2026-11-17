---
id: creative-arts.animation.visual-development.light-halftone-core-shadow
name: light-halftone-core-shadow
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, form-principle, core-shadow, terminator, halftone, value-structure]
level: intro
status: draft
description: "Render form with the light-to-shadow sequence: highlight, light, halftone, terminator, core shadow, reflected light and cast shadow, kept in two value families."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://books.google.com/books?vid=ISBN9781933492964
  - https://en.wikipedia.org/wiki/Terminator_(solar)
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Light, halftone, core shadow and terminator

Goal: forms that turn convincingly under one light, following Gurney's form principle:
the tone of a surface depends on the angle it faces relative to the light.

## The sequence on a sphere (lit side to shadow side)
1. **Highlight**: specular reflection of the source (depends on material).
2. **Light/centre light**: plane facing the light, lightest diffuse value.
3. **Halftone**: planes turning away; values darken gradually.
4. **Terminator**: the line where light stops reaching; on soft light it is a gradient,
   on hard light a sharp edge.
5. **Core shadow**: darkest band just past the terminator, before reflected light.
6. **Reflected light**: bounce from nearby surfaces lifts the shadow slightly - but it stays
   darker than any value in the light.
7. **Cast shadow**: shadow thrown onto other surfaces (see cast shadows skill).

## The two-family rule
Keep every value in light separate from every value in shadow. The darkest halftone must
be lighter than the lightest reflected light. Breaking this flattens form (Gurney,
Robertson).

## Method
1. Decide light direction, hardness and colour.
2. Separate light and shadow with a flat two-value pass (find the terminator on each form).
3. Model the halftones inside the light family only.
4. Add core shadow, then subtle reflected light within the shadow family.
5. Add highlights last, sized by material.

## Failure modes
- Reflected light as bright as the halftones - "plastic" or double-lit look.
- Gradients spread evenly across the whole form instead of turning at the terminator.
- Terminator hardness inconsistent with the light source size.

## Verify
- [ ] Two-value pass reads the forms on its own.
- [ ] Shadow family darker than light family everywhere.
- [ ] Terminator edge matches the source size.

Related: `creative-arts.animation.visual-development.cast-shadows`,
`creative-arts.animation.blender.cel-light-direction`.
