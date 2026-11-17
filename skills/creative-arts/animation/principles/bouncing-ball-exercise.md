---
id: creative-arts.animation.principles.bouncing-ball-exercise
name: bouncing-ball-exercise
category: creative-arts
field: animation
product: principles
tags: [animation, bouncing-ball, squash-and-stretch, spacing, timing, decay, gravity, arcs, exercise, 2d, cg]
level: intro
status: draft
description: "Animate the bouncing ball to a pro standard: parabolic arcs, gravity spacing, squash on contact only, stretch at speed, and decaying bounce heights and frame counts."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bouncing ball exercise

Goal: a ball that reads as a specific material and weight dropping under gravity. Every
studio test and every curriculum (CalArts Animation I, Sheridan year 1, Gobelins entry
portfolio) starts here because it isolates timing, spacing, arcs and squash/stretch with no
acting to hide behind.

## Method (24 fps, rubber ball, drawn or keyed)
1. **Plan the path first.** Draw the arcs as a series of parabolas, each lower and shorter
   than the last. Contacts sit on the ground line; apexes sit at the top of each parabola.
   Horizontal travel per bounce shrinks with height.
2. **Key contacts and apexes only.** First bounce: apex to contact about 10-12 frames for a
   drop from roughly 3 ball-heights; each later bounce takes fewer frames (heights decay
   roughly 30-50 % per bounce for rubber, more for a heavy or soft ball).
3. **Gravity spacing.** Spacing is tight at the apex and wide near contact. Approximate with
   odd-number ratios from the apex down: 1, 3, 5, 7... units (constant acceleration). In CG
   this is a vertical curve with flat (ease) tangents at apex and broken, sharp tangents at
   contact - never an ease into the ground.
4. **Horizontal is near-linear.** Forward motion loses a little at each contact but has no
   ease in the air. Keep X on linear or nearly linear interpolation separate from Y.
5. **Squash only on the contact frame(s).** One frame of squash, flattened along the ground,
   width increasing to preserve volume. A rubber ball may hold 1-2 frames; a bowling ball
   gets none.
6. **Stretch at the fast frames only.** The frame before and after contact stretches along the
   direction of travel (along the arc tangent, not vertically). No stretch near the apex.
7. **Decay to rest.** Final bounces become 2-4 frame hops, then a short roll and stop with a
   slight settle.

## Material calibration
| Ball | Squash | Bounce decay | Frames first bounce |
|---|---|---|---|
| Rubber | strong, 1-2 frames | slow (many bounces) | 10-12 |
| Tennis | medium | medium | 9-11 |
| Bowling | none / subtle | 1-2 tiny bounces | fast drop, short |
| Beach ball | soft, slow recovery | floaty, more hang | 14+ |

## Failure modes
- Ease into the contact: the ball "lands softly" and looks like it is on a string. Contact
  frames need the widest spacing.
- Squash on the frame before contact: the ball deforms in mid-air. Squash belongs on the frame
  where it touches.
- Stretch pointing straight up on an arcing ball: rotate the stretch axis to the path.
- Same frame count every bounce: reads as a looped animation, not gravity.
- Volume loss: a squashed ball that does not widen looks like it shrank.

## Verify
- [ ] Scrub with onion skin: spacing tight at apex, widest at contact.
- [ ] Each bounce is lower AND shorter in frames than the one before.
- [ ] Squash appears only on contact frames; stretch only on the fastest frames.
- [ ] Area of the squashed and stretched ball matches the round ball (overlay check).
- [ ] Swap to a bowling-ball setting and the same path reads heavier by timing alone.

Related: `creative-arts.animation.principles.squash-and-stretch-in-production`,
`creative-arts.animation.principles.applying-timing-and-spacing`,
`creative-arts.animation.principles.arc-tracking`.
