---
id: creative-arts.animation.production-design.hero-vs-background-props
name: hero-vs-background-props
category: creative-arts
field: animation
product: production-design
tags: [production-design, prop-design, hero-vs-background-props, asset-tiers, level-of-detail]
level: practitioner
status: draft
description: "Decide hero vs background treatment for props: detail level, polycount and texture budgets, rig and colour model needs, and when a background prop must be promoted."
sources:
  - https://animationguild.org/
  - https://www.khanacademy.org/computing/pixar
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hero props vs background props

Goal: spend design and build effort where the camera and story look.

## 1. Classify
| Tier | Definition | Design deliverable |
|---|---|---|
| Hero | handled, featured in close-up, plot-relevant | full orthos, callouts, colour model per lighting state, states |
| Mid | seen clearly but not handled | turnaround or 2 views, materials |
| Background | dressing, seen at distance | silhouette and colour within the set palette, often library |
Classification comes from the asset breakdown and boards (closest camera distance).

## 2. Visual hierarchy
- Hero props have more contrast, saturation or unique shape than the background props around them,
  so they are found instantly when they matter.
- Background props stay within the environment palette and simpler shapes; they must not compete.

## 3. Budget
- Hero: higher texture resolution, rig if it moves, deformation if handled.
- Background: shared materials, instancing, low detail; one design serves many shots.

## 4. Promotion and demotion
- When boards add a close-up or interaction with a background prop, promote it and redesign or detail it.
  Track this in the breakdown; a mid-production promotion is a schedule event.

## Verify
- [ ] Each prop has a tier from the breakdown.
- [ ] Hero props stand out from surrounding dressing.
- [ ] Promotions logged.

Related: `creative-arts.animation.production-design.prop-design`,
`creative-arts.animation.production-design.script-asset-breakdown`,
`creative-arts.animation.production-design.set-dressing`.
