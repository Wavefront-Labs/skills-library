---
id: creative-arts.animation.visual-development.occlusion-shadows
name: occlusion-shadows
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, form-principle, occlusion-shadow, ambient-occlusion, contact-shadow, grounding]
level: practitioner
status: draft
description: "Paint occlusion shadows: dark accents where ambient light is blocked - contacts, crevices, under objects - which ground forms in both light and shadow."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Ambient_occlusion
  - https://books.google.com/books?vid=ISBN9781933492964
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Occlusion shadows

Goal: small dark accents in tight spaces that make objects sit on surfaces and give
form solidity. Gurney: "occlusion shadows are the darkest darks" where light from the sky or
room cannot reach.

## Where they occur
- Under an object resting on a surface (shoe on floor, cup on table).
- Corners where walls meet floors, creases, deep folds, between fingers, lips meeting.
- Inside small openings (nostrils, keyholes, ear canals).
- They appear even on overcast days when no cast shadow exists.

## Rules
- Darkest where the gap is narrowest; fades as the space opens up.
- Present in both the light and the shadow side (they come from blocked ambient, not the key).
- Size small: a thin dark line or wedge, not a big soft blob.
- Warm or neutral dark, often slightly more saturated than surrounding shadow.

## Method
1. After the light/shadow pass, identify every contact point and crevice.
2. Add a thin, dark accent hugging the contact; soften outward over a short distance.
3. Check overall value: occlusion darks should be the darkest notes only in tiny areas.
4. In CG, an AO pass multiplied in compositing does the same; dial strength so it does not
   grey out the whole image.

## Failure modes
- Objects floating because the contact accent is missing.
- AO dirt everywhere (multiplied too strong), muddying lit areas.
- Big soft halos instead of tight accents.

## Verify
- [ ] Every contact has an occlusion accent.
- [ ] Accents narrow and darkest at the tightest gap.
- [ ] Overall image not greyed by AO.

Related: `creative-arts.animation.visual-development.cast-shadows`,
`creative-arts.animation.blender.ambient-occlusion-node`.
