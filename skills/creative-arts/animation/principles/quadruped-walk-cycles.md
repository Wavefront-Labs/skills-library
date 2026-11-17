---
id: creative-arts.animation.principles.quadruped-walk-cycles
name: quadruped-walk-cycles
category: creative-arts
field: animation
product: principles
tags: [animation, animal-locomotion, quadruped-walk, dog-walk, cat-walk, quadruped, digitigrade, shoulder-blades, cycles, creature-animation]
level: practitioner
status: draft
description: "Animate dog and cat walk cycles: lateral-sequence footfalls, front and back legs as two offset bipeds, shoulder blade and hip motion, and species differences."
sources:
  - https://books.google.com/books?vid=ISBN9780486202037
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quadruped walk cycles

Goal: believable four-legged walks for dogs, cats and similar animals.

## Footfall
Most quadrupeds walk in a **lateral sequence**: LH, LF, RH, RF. A practical way to animate it:
treat the animal as **two bipeds** - the back pair walks like a person, the front pair walks the
same cycle offset by about a quarter cycle (the front foot on the same side lands shortly after
the hind foot).

## Anatomy that drives the motion
- **Digitigrade legs** (dog, cat): they walk on toes; the "backward knee" on the hind leg is the
  ankle (hock); the front "knee" is the wrist.
- **Shoulder blades** slide and rotate: when a front leg is planted and the body passes over it,
  the shoulder blade rises above the spine line (very visible on cats).
- **Hips** tilt and rise over the planted hind leg.
- **Spine** flexes laterally between shoulder and hip motion.
- **Head** nods with front-foot contacts (more in larger animals), stable for hunters stalking.
- **Tail** overlaps the hip motion (wave principle).

## Species differences
| Animal | Character |
|---|---|
| Dog (medium) | 12-16 frames per step cycle half; head bob, tail wag overlaid |
| Cat | lower, smooth, shoulder blades prominent, hind foot lands in front paw's print (direct register) |
| Elephant | slow (about 2 s cycle), huge weight, legs columnar, feet spread on contact |

## Method
1. Animate the hind pair as a cycle (contacts, passing, push).
2. Copy timing to the front pair with an offset; adjust contacts to the footfall order.
3. Add body: hips rise over planted hind, shoulders rise over planted front.
4. Add spine, neck/head, tail overlap.

## Failure modes
- Legs moving like a table (diagonal pairs locked): reads as a trot.
- No shoulder blade motion: stiff, toy-like.
- Feet sliding - match cycle speed to stride.

## Verify
- [ ] Lateral-sequence footfall order.
- [ ] Shoulder and hip rise over the planted leg.
- [ ] Tail and head overlap, not locked.

Related: `creative-arts.animation.principles.horse-gaits`,
`creative-arts.animation.principles.cycles-and-foot-slip`.
