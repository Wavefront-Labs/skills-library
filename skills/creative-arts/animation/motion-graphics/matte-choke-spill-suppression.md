---
id: creative-arts.animation.motion-graphics.matte-choke-spill-suppression
name: matte-choke-spill-suppression
category: creative-arts
field: animation
product: motion-graphics
tags: [spill-suppression, keying, matte-choker, simple-choker, advanced-spill-suppressor, edge-fringe, light-wrap, after-effects, matte-cleanup]
level: practitioner
status: draft
description: "Finish keyed mattes in After Effects: choke and spread edges, remove green/blue spill from skin and hair, and add light wrap so subjects sit in the new background."
sources:
  - https://helpx.adobe.com/after-effects/using/keying-effects.html
  - https://helpx.adobe.com/after-effects/using/matte-effects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matte choking and spill suppression

**Goal:** a keyed subject without dark/bright outlines or green cast, blending naturally into its new
background.

## Choking the matte

- **Simple Choker** (Effect - Matte): Choke Matte positive shrinks the matte (removes fringe), negative
  spreads it. Use small values (0.5-2 px).
- **Matte Choker**: two-stage choke with geometric softness; good for rounding chewed edges then
  pulling them in.
- **Refine Soft Matte / Refine Hard Matte**: edge-aware refinement with motion blur and decontamination.
Choke only after a good key: chokes fix 1-2 px fringes, not a bad key.

## Spill suppression

Green screen bounces green onto skin, hair, shoulders and reflective props.
- **Advanced Spill Suppressor** (Effect - Keying): Method Standard (auto) or Ultra (with colour choice
  and tolerance); good default.
- Keylight's own Despill Bias / Alpha Bias controls in the effect.
- Manual: Hue/Saturation targeting greens or a Channel-based despill (limit green to the average of red
  and blue) for stubborn cases.
Check skin tones on a vectorscope: they should sit near the skin-tone line, not pulled toward green.

## Light wrap

Edges of a real subject pick up light from the background. Recreate:
1. Duplicate the background, blur it.
2. Use the subject's inverted alpha, blurred, intersected with the subject's alpha to get an edge band.
3. Screen/Add the blurred background through that band over the subject at low opacity.
(Plugins such as Light Wrap in many packs do this; the logic is the same.)

## Gotchas

- Over-despill turns skin grey or magenta; check whites (shirts) and skin together.
- Choking motion-blurred edges removes the blur; refine those areas with Refine Soft Matte instead.
- Apply despill before colour grading the subject, so the grade is not fighting green.

## Verify

Over black, white and the final background at 200%: no green edges, no dark halo, skin hue on the
vectorscope's skin line, hair edges keep detail.
