---
id: creative-arts.animation.principles.run-cycle-key-poses
name: run-cycle-key-poses
category: creative-arts
field: animation
product: principles
tags: [animation, run-cycle, run-key-poses, runs, airborne, contact, push-off, locomotion, cycles, sprint]
level: practitioner
status: draft
description: "Animate a run cycle: contact, down, push-off and airborne positions, why runs have frames with no foot on the ground, and timing from jog to sprint."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Walk_cycle
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run cycle key poses

Goal: a run with power and hang. The defining difference from a walk: there are frames with
both feet off the ground, and the body is lowest at the down after contact.

## Positions (one step)
1. **Contact** - front foot strikes under or slightly ahead of the body; body leaning forward.
2. **Down** - lowest point; supporting knee bent, absorbing weight; free leg folding tight
   under the hip (heel near the buttock in a fast run).
3. **Push-off (passing/up)** - supporting leg extends, driving forward; free knee drives up.
4. **Airborne** - both feet off the ground; body at its highest; legs at their widest split.
5. Next contact.

## Timing at 24 fps
| Run | Frames per step |
|---|---|
| Sprint/cartoon zip | 3-4 |
| Fast run | 5-6 |
| Normal run | 6-8 |
| Jog | 8-10 |
Airborne frames: 1-3 in a normal run, more in a bounding run.

## Body and arms
- Forward lean increases with speed.
- Arms pump strongly, bent about 90 degrees, opposite to legs; hands drive higher in front.
- Less vertical bounce than you think in a sprint - the energy goes forward; a jog bounces more.

## Failure modes
- No airborne frame: looks like a fast walk.
- Body highest on contact: floaty.
- Arms swinging across the body excessively (wastes energy, reads as flailing - unless comic).
- Feet sliding at contact (cycle ground speed mismatch).

## Verify
- [ ] At least one frame with no ground contact per step.
- [ ] Lowest point is the down after contact.
- [ ] Forward lean appropriate to speed.

Related: `creative-arts.animation.principles.jump-phases`,
`creative-arts.animation.principles.cycles-and-foot-slip`.
