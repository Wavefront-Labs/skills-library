---
id: creative-arts.animation.principles.successive-breaking-of-joints
name: successive-breaking-of-joints
category: creative-arts
field: animation
product: principles
tags: [animation, follow-through-overlap, successive-breaking-of-joints, flexibility, overlap, drag, joints, arm-swing, broken-joints]
level: advanced
status: draft
description: "Apply Milt Kahl's successive breaking of joints: joints bend backward against their natural direction as force passes through a limb, for flexible, whip-like arms and bodies."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9780786860708
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Successive breaking of joints

Goal: make limbs feel flexible and alive by letting each joint lag and briefly bend the
"wrong" way as the motion travels through it. Williams credits Milt Kahl and Art Babbitt with
the term; it is the core of the Survival Kit's "Flexibility" section.

## How it works
Force starts at the root (shoulder) and passes outward. Each joint is dragged by the previous
one, so for a moment it trails behind - and in a fast move, bends backward past straight.
- Arm swinging forward: shoulder leads, elbow lags, the wrist bends *back* (palm trailing),
  then snaps forward when the elbow stops.
- Hand flick: the wrist breaks back as the forearm moves, fingers break back as the wrist moves.
- Body: hips lead, spine curves back, head drags.

## Method
1. Animate the root joint's motion first (layered thinking).
2. On the next joint, delay its rotation 1-3 frames and, at the moment the parent accelerates,
   rotate it opposite to the travel direction (the break).
3. When the parent decelerates or stops, the child overshoots in the travel direction.
4. Repeat for each joint outward; the offset accumulates.
5. Keep the break within the style: realistic joints never hyperextend visibly - break
   wrists and fingers, not elbows; cartoon styles may break elbows too.

## CG notes
- FK arms show this naturally with rotation offsets; IK arms need the wrist break keyed
  explicitly.
- Elbow breaks backward look like a rig bug on realistic characters - disable or limit.

## Failure modes
- All joints rotating together: a stiff, wooden "hinge" arm.
- Breaks on slow moves: looks injured. Use it on accelerations.
- Uniform offsets on every joint: reads mechanical; vary the delay with mass.

## Verify
- [ ] Frame-step a fast arm move: the wrist visibly trails then overtakes.
- [ ] The break happens on acceleration, the overshoot on deceleration.
- [ ] No impossible hyperextension for the style.

Related: `creative-arts.animation.principles.wave-and-whip-action`,
`creative-arts.animation.principles.designing-the-breakdown`.
