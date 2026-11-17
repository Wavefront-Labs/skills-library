---
id: creative-arts.animation.art-direction.shot-to-shot-color-continuity
name: shot-to-shot-color-continuity
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, visual-continuity, color-continuity, grading, sequence-review]
level: advanced
status: draft
description: "Keep colour continuous across the shots of a sequence: reference frames, sequence contact sheets, scopes, and where to fix drift (lighting, comp or grade)."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9781138014152
  - https://en.wikipedia.org/wiki/Continuity_editing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shot-to-shot color continuity

Goal: within a scene, cuts change the camera, not the light or colour, unless the story asks for a change.

## 1. Establish references
- Pick a **reference frame** per sequence (usually the approved master shot) and save it as a still.
- List the colour-critical elements: sky, key light colour, skin, hero costume, a large set surface.

## 2. Review as a sequence, not as shots
- Build a **contact sheet**: one frame per shot in cut order (first, middle or most representative frame).
  Scan it left to right; drift is obvious side by side and invisible one shot at a time.
- Play the cut with handles; flashes of different white balance across a cut are the most visible error.
- Check scopes: vectorscope for hue/saturation of skin and neutrals, waveform for black and white points.
  Skin should sit near the skin-tone line consistently in the same light.

## 3. Common causes and where to fix
| Cause | Fix at |
|---|---|
| Light rig differs between shots | lighting: push shared rig/light-link presets per sequence |
| Background painted at different times | BG: repaint to reference or match in comp |
| Render settings differ (exposure, AO) | lighting template/render preset |
| Small residual drift | grade: per-shot trim toward the reference |
Fix upstream when the error repeats across many shots; trim in the grade only for the residual.

## 4. Intentional change
- If light changes within a scene (lamp switched on, sunset progressing), plan it as a progression
  on the contact sheet so it reads as story, not error.

## Verify
- [ ] Reference frame per sequence stored with the shots.
- [ ] Contact sheet reviewed in cut order.
- [ ] Skin and neutrals consistent on scopes across cuts.

Related: `creative-arts.animation.color.color-grading`,
`creative-arts.animation.editorial.continuity-supervision`,
`creative-arts.animation.art-direction.value-matching-across-cuts`.
