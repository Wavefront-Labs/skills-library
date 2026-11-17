---
id: creative-arts.animation.principles.center-of-gravity-and-balance
name: center-of-gravity-and-balance
category: creative-arts
field: animation
product: principles
tags: [animation, weight-animation, center-of-gravity, balance, base-of-support, posing, weight, plumb-line, cog]
level: intro
status: draft
description: "Keep poses balanced by placing the centre of gravity over the base of support, check it with a plumb line, and use deliberate imbalance to start motion."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Center_of_mass
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Centre of gravity and balance

Goal: characters look grounded when still and motivated when moving. Balance is the
most-checked thing in weight notes.

## Rules
1. **Static balance**: the centre of gravity (roughly the pelvis/navel area in a standing human)
   sits vertically above the base of support (the area under and between the feet).
2. **Single support**: on one foot, the CoG must be over that foot - hips shift over it.
3. **Carrying weight**: the combined CoG (body + load) must be over the feet - lean away from the load.
4. **Movement starts with imbalance**: walking is controlled falling - the CoG moves ahead of
   the support, a foot catches it.
5. **Different body shapes**: a big belly or a heavy upper body moves the CoG; recompute
   by eye for each design.

## Plumb line check
- Draw a vertical line down from the pit of the neck (front view) or from the ear/shoulder
  (side view) - it should land within the base of support in a balanced static pose.
- CG: add a vertical guide object constrained to the hips or use a CoG indicator from the rig.

## Uses of imbalance
- Leaning poses that hold only because the character is pushing on something.
- Comedy: a character frozen off-balance (cartoon physics) for a beat before falling.
- Anticipation: shift weight before stepping.

## Failure modes
- Standing poses that would fall over.
- Hips centred between feet when the character is on one leg.
- Characters carrying loads without counter-lean.

## Verify
- [ ] Plumb line lands in the base of support on every static key.
- [ ] Moving poses lead with the CoG.
- [ ] Load-carrying poses counter-lean.

Related: `creative-arts.animation.principles.weight-shift-in-standing-poses`,
`creative-arts.animation.character-design.character-design-craft`.
