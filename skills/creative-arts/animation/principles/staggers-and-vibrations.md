---
id: creative-arts.animation.principles.staggers-and-vibrations
name: staggers-and-vibrations
category: creative-arts
field: animation
product: principles
tags: [animation, timing-principle, stagger-vibration, stagger, vibration, impact, twang, exposure-sheet, cartoon, timing]
level: practitioner
status: draft
description: "Animate staggers and vibrations (twangs, shudders, impacts) with Williams' stagger exposure patterns that alternate drawings to make energy decay."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Staggers and vibrations

Goal: show a quivering object or character - an arrow twanging in a target, a diving board after
a jump, a character shuddering with cold or shock - using alternating drawings timed so the
vibration decays.

## The stagger (Williams)
Instead of animating every position, you animate a normal move and then re-expose drawings in
a back-and-forth order on the exposure sheet so the object jitters between positions with
decreasing amplitude.
- Draw the move from rest (A) to extreme (B), say drawings 1-9.
- Expose a vibrating sequence like 1, 9, 3, 7, 4, 6, 5 - alternating ends, closing toward the middle.
- On ones for a fast twang; each pair can repeat to slow it.

## Vibration
- Two or three extreme drawings alternated every frame (A, B, A, B) give a high-frequency buzz;
  reduce amplitude by switching to closer pairs over time.
- Add a motion-blur line or a multiple on the extremes for very fast vibration.

## CG method
1. Key rest and two extremes.
2. Key an alternating, decaying sequence on ones (each extreme closer to rest).
3. Or use a noise/damped-sine driver: amplitude * e^(-k t) * sin(2 pi f t). Blender: an F-Curve
   Noise modifier with keyed influence, or a driver expression; keep frequency below about half
   the frame rate (Nyquist) or it aliases into random noise.

## Uses
- Shock takes: the whole body staggers after an impact.
- Cold shivers: low-amplitude, irregular vibration with stillness gaps.
- Mechanical: engine idle, phone buzz.

## Failure modes
- Constant amplitude: never ends.
- Frequency too high on CG noise (aliasing).
- Vibrating the whole character when only a part should.

## Verify
- [ ] Amplitude decays to rest within the planned frames.
- [ ] At speed reads as vibration, not a flicker.
- [ ] Exposure sheet or keys show the decaying alternation.

Related: `creative-arts.animation.principles.applying-timing-and-spacing`.
