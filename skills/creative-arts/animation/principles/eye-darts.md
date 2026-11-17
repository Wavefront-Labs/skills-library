---
id: creative-arts.animation.principles.eye-darts
name: eye-darts
category: creative-arts
field: animation
product: principles
tags: [animation, acting-for-animation, eye-darts, saccades, eye-direction, eyes, convergence, close-up, polish, facial-animation]
level: practitioner
status: draft
description: "Animate eye darts (saccades) and eye direction in close-ups: timing, patterns when looking at a face, convergence, and lids following the eyes."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Saccade
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eye darts

Goal: eyes that look alive and thinking. Real eyes move in saccades - fast jumps of 20-200 ms
with fixations between - not smooth pans.

## Timing at 24 fps
- A dart: **1-2 frames** of movement (often 1 frame for small darts, 2 with one inbetween for
  larger), then a hold.
- Holds between darts: 6-30 frames, irregular.
- Big eye changes (over about 20 degrees) usually involve a head move and often a blink.

## Patterns
- **Looking at a face**: darts between the other person's eyes (left eye, right eye) and
  occasionally to the mouth. Small amplitude.
- **Thinking/recalling**: eyes move away from the listener, often up or to the side, with
  a few small darts, then return.
- **Lying/hiding**: eye contact broken at specific moments (do not overuse).
- **Scanning a room**: a series of fixations with darts, not a smooth pan.

## Technical rules
- **Convergence**: both eyes point at the same target; at close distances they cross slightly.
  Use an aim/look-at target in CG rather than rotating eyes separately.
- **Lids follow**: upper lid follows the iris top when looking up/down - a lid that stays put
  while the eye rotates down looks surprised.
- **Pupils** stay the same size during darts (except lighting/emotion changes).

## Failure modes
- Smooth, interpolated eye moves: dead or sleepy.
- Darts on a regular interval: mechanical.
- Walleye/crosseye from independent eye rotation.
- Darts during key emotional stares (keep those still).

## Verify
- [ ] Darts are 1-2 frames, holds irregular.
- [ ] Both eyes converge on the target.
- [ ] Lids track vertical eye rotation.

Related: `creative-arts.animation.principles.eyes-lead-the-action`,
`creative-arts.animation.principles.blink-timing`.
