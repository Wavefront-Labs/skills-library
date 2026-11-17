---
id: creative-arts.animation.principles.pencil-tests-and-registration
name: pencil-tests-and-registration
category: creative-arts
field: animation
product: principles
tags: [animation, hand-drawn-pipeline, pencil-test, line-test, peg-bar, registration, field-guide, scanning, 2d, digital-2d]
level: intro
status: draft
description: "Keep hand-drawn work registered (peg bars, field guides, digital canvas setup) and shoot pencil/line tests to check timing before cleanup."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pencil tests and registration

Goal: every drawing lines up with every other and with the background, and timing is checked
on a pencil (line) test before expensive cleanup.

## Registration
- **Paper**: Acme peg bar (centre round hole, two flat slots) is the industry standard; all
  paper punched the same; drawings and layouts on the same pegs.
- **Field guide**: a 12-field (or 10/16) grid defines the camera frame and moves; layouts, BGs
  and animation all reference it.
- **Digital** (Toon Boom Harmony, TVPaint, Krita, Blender Grease Pencil): fixed canvas size and
  camera frame identical across scenes; never resize the canvas mid-scene; field guide overlay
  available in the camera view.
- **Scanning paper**: use a peg bar on the scanner; auto-align on peg holes in the software
  (e.g. Harmony's scan module) to avoid drift.

## Pencil test
1. Shoot/scan the rough or key drawings at the exposures on the x-sheet (twos as twos).
2. Play with the dialogue/music track.
3. Review: timing, spacing, arcs, staging - not drawing quality.
4. Iterate before tie-downs and cleanup.
5. Keep versions (v01, v02) so the director can compare.

## Failure modes
- Drawings drifting position between frames (no pegs / scan alignment).
- Pencil test shot on ones when the sheet says twos - false timing.
- Skipping tests and finding timing problems after cleanup.

## Verify
- [ ] Flip test: static parts (a held background prop) do not jitter.
- [ ] Pencil test exposures match the x-sheet.
- [ ] Director approved the test before cleanup started.

Related: `creative-arts.animation.principles.tie-down-drawings`,
`creative-arts.animation.storyboarding.trucks-and-dollies`.
