---
id: creative-arts.animation.environment-design.water-surfaces-and-reflections
name: water-surfaces-and-reflections
category: creative-arts
field: animation
product: environment-design
tags: [environment-design, natural-environment, water-design, reflections, water-painting, stylized-water]
level: practitioner
status: draft
description: "Design water surfaces and reflections: reflection geometry, Fresnel darkening near the viewer, ripple breakup, transparency and stylized wave patterns."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Fresnel_equations
  - https://en.wikipedia.org/wiki/Specular_reflection
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Water surfaces and reflections

Goal: water that reads as water in the show style - lakes, rivers, puddles, sea - with
correct reflection logic.

## Physics to respect
- **Reflections are vertical**: an object's reflection sits directly below it, mirrored about
  the waterline at its base (not the shoreline in front of it). Objects set back from the
  shore show a shortened reflection or none.
- **Fresnel**: looking straight down, water is transparent/dark and you see the bottom;
  at grazing angles (far away) it reflects the sky strongly and gets lighter.
- **Values**: reflections of light objects are slightly darker; reflections of dark objects
  slightly lighter (Gurney).
- **Ripples** stretch reflections vertically and break them into horizontal bands; wind lines
  are matte (sky-reflecting) streaks.
- **Colour**: shallow water shows the bed colour (green, tan); deep water the sky and
  absorption colour (blue-green).

## Stylization
Pick a vocabulary: graphic wave shapes and highlight lines (UPA/Ghibli sea), painted
reflections with horizontal breakup, or flat colour with animated sparkle overlays. Water
that moves must be planned for animation/FX: cycles of ripples, highlight shapes on 2s.

## Method
1. Find the waterline under each object; draw mirrored shapes there.
2. Grade the surface from transparent/dark near camera to reflective/light far away.
3. Break reflections with horizontal ripples; add wind lines.
4. Add edge foam/wet bands at shores.

## Failure modes
- Reflections offset sideways or mirrored at the wrong line.
- Uniform flat blue water.
- Reflections as bright as the objects.

## Verify
- [ ] Reflections directly below objects.
- [ ] Near-to-far Fresnel gradient.
- [ ] Ripple breakup horizontal.

Related: `creative-arts.animation.blender.fluid-water-fx`,
`creative-arts.animation.visual-development.specular-highlights-and-material-read`.
