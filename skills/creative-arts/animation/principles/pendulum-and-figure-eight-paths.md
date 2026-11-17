---
id: creative-arts.animation.principles.pendulum-and-figure-eight-paths
name: pendulum-and-figure-eight-paths
category: creative-arts
field: animation
product: principles
tags: [animation, motion-arcs, pendulum-arc, figure-eight, cycles, swing, overlap, exercise, pendulum]
level: intro
status: draft
description: "Animate pendulum swings and figure-eight paths: gravity spacing at the bottom of the arc, drag on attached weights, and using the figure-eight for cycles and overlap."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Pendulum
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pendulum and figure-eight paths

Goal: master the two most reusable arc shapes. The pendulum is a standard animation-school
exercise (spacing on an arc, overlap on a chain); the figure-eight is the path tips trace in
almost every cycle.

## Pendulum
- Path: an arc centred on the pivot.
- Spacing: slowest at the two extremes, fastest at the bottom (gravity). Ease into and out of
  each extreme; no ease at the bottom.
- Period: real pendulum period T = 2 * pi * sqrt(L / g). A 1 m pendulum takes about 2 s per full
  swing (48 frames at 24 fps). Cartoon timing can cheat but the ratio of length to period
  sells scale - long pendulums must swing slowly.
- Decay: amplitude reduces slowly unless pushed.

## Pendulum with a soft weight (overlap exercise)
Hang a flexible tail/rope or a soft bob: the attached part drags behind on each change of
direction and overshoots at the extremes - the exercise teaches overlap on a predictable path.

## Figure-eight
- The tip of anything driven back-and-forth by its base (a flag edge, a tail, a hand in a walk,
  a wing tip) traces a loop or figure-eight because the base changes direction before the tip.
- In walks, the hand traces a flattened figure-eight/oval in side view; the head traces a small
  figure-eight in front view from the lateral sway and the bounce.

## Method
1. Animate the base/pivot motion.
2. Add the tip with offset; check the trail: it should loop, not retrace a line.
3. Adjust offset until the loop is open but not wild.

## Failure modes
- Even spacing on a pendulum: reads as a motor.
- Fast swing on a long pendulum: scale feels tiny.
- Tips retracing the same line in cycles: no overlap.

## Verify
- [ ] Spacing is widest at the bottom of the swing.
- [ ] Period matches the length (or the intended cheat is consistent).
- [ ] Tip trails form loops in cycles.

Related: `creative-arts.animation.principles.wave-and-whip-action`,
`creative-arts.animation.principles.arc-tracking`.
