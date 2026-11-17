---
id: creative-arts.animation.principles.stretch-limits-on-rigid-subjects
name: stretch-limits-on-rigid-subjects
category: creative-arts
field: animation
product: principles
tags: [animation, rigid-body-stretch-limits, squash-and-stretch, realism, mechanical, props, vehicles, photoreal, cheats, motion-blur]
level: practitioner
status: draft
description: "Decide how much squash and stretch rigid or realistic subjects (props, vehicles, realistic humans) can take, and the cheats that give the same snap without deformation."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stretch limits on rigid subjects

Goal: get the energy of squash and stretch on things that must not visibly deform - a car, a
sword, a realistic human, a logo - without breaking believability.

## Decide the budget first
| Subject | Visible deformation allowed |
|---|---|
| Cartoon prop with a face / personality | full squash and stretch |
| Stylized hard prop (hammer, phone) | 0-5 %, only on the impact frame |
| Vehicles in stylized feature | body flex 2-10 % on bumps/launch, wheels stay round |
| Photoreal creature/human | none as geometry; flesh jiggle and muscle via sims |
| Logos/brand marks | ask the client; usually none |

## Cheats that deliver the feel without deformation
1. **Suspension and pivots** - let parts of a rigid object move relative to each other
   (car body dips on springs, lid lags the box, blade flexes in its handle).
2. **Camera shake and frame impact** - shake the camera or hold an impact frame instead of
   squashing the object.
3. **Spacing** - a rigid object can still have extreme spacing; a 1-frame snap reads as
   impact.
4. **Motion blur / speed lines** - streak the fast frames instead of stretching geometry.
5. **Secondary elements** - dust, sparks, a cloth flag, a dangling keychain carry the
   squash and stretch for the rigid object.
6. **Hidden one-frame stretch** - a 1-frame stretch along the motion on a very fast move is
   invisible at speed but adds snap; check it in stepped playback.

## Realistic humans
Do not stretch bone lengths. Get "squash" from spine compression, knees bending, shoulders
rising, and flesh: cheeks pushing up, belly compressing on a landing. The principle survives
as overlap and compression, not as scaling.

## Failure modes
- Wheels or round parts going oval: the eye catches it immediately.
- Stretching a realistic limb: reads as a rig bug.
- Removing all of it: rigid animation looks floaty. Replace it with spacing and secondary.

## Verify
- [ ] Freeze each frame: rigid parts keep their proportions (or within the budget table).
- [ ] At speed, impacts still feel sharp.
- [ ] The style lead or client has signed off the deformation budget.

Related: `creative-arts.animation.principles.squash-and-stretch-in-production`,
`creative-arts.animation.principles.smear-frames-and-multiples`.
