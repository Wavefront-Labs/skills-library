---
id: creative-arts.animation.principles.settles-and-recoil
name: settles-and-recoil
category: creative-arts
field: animation
product: principles
tags: [animation, follow-through-overlap, settle-frames, recoil, overshoot, follow-through, moving-hold, landing, stop]
level: practitioner
status: draft
description: "Finish actions with overshoot, recoil and settle: frame counts, amplitude by weight, and how to hand off into a living moving hold instead of a dead stop."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Settles and recoil

Goal: actions end the way physical bodies end - they overshoot, come back, and settle -
rather than freezing on the final key.

## Pattern
1. **Hit** - the action arrives at its destination (or impact).
2. **Overshoot** - the mass carries past (a pointing arm goes slightly beyond, a body landing
   sinks lower than its rest).
3. **Recoil** - it comes back, slightly past rest in the other direction for light/springy
   characters.
4. **Settle** - into the final pose, usually with a moving hold.

## Frame ranges at 24 fps
| Action | Overshoot | Settle |
|---|---|---|
| Arm point stop | 2-3 frames, 5-10 % past | 4-8 frames |
| Body landing from a jump | 3-6 frames compress | 6-14 frames |
| Head turn stop | 1-3 frames | 4-6 |
| Heavy character stop | small overshoot, slow settle | 10-20 |

## Method
1. Key the hit pose on the frame it should read.
2. Add an overshoot key a few frames later; parts further from the root overshoot later and
   farther (follow-through).
3. Add the settle key; break the settle into a moving hold (2-5 % continued drift over the hold).
4. Stagger settles by body part: hips settle first, head and arms last.

## Failure modes
- Overshoot on everything: bouncy, rubbery characters when the style is grounded.
- Settle too long: the next action feels delayed.
- Overshoot in IK space causing elbows to snap or feet to slide.

## Verify
- [ ] Every action that stops has a visible but proportionate settle.
- [ ] Extremities settle after the core.
- [ ] Holds after settles drift slightly (not frozen).

Related: `creative-arts.animation.principles.appendage-overlap`,
`creative-arts.animation.principles.hold-timing`.
