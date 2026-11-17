---
id: creative-arts.animation.principles.designing-the-breakdown
name: designing-the-breakdown
category: creative-arts
field: animation
product: principles
tags: [animation, pose-to-pose-method, breakdown-pose, passing-position, arcs, overlap, head-turn, personality, inbetween]
level: practitioner
status: draft
description: "Design the breakdown pose between two keys to shape the arc, lead and drag, so a move gets character instead of a mechanical 50 percent blend."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing the breakdown

Goal: the breakdown is the most creative single drawing in a move. Williams calls it the
"passing position"; it decides whether a head turn dips or rises, whether an arm leads or
drags, whether the action has weight.

## Method
1. Look at the two keys and ask: **which part leads and which drags?** The breakdown shows it -
   a head turn with the nose leading, hair and ears dragging; an arm swing with the wrist
   dragging behind the elbow.
2. **Choose the path**: a head turn breakdown goes down (a dip, natural) or up (alert, surprised).
   A hand moving across goes on a curve, never the straight line.
3. **Choose the favour**: place the breakdown off-centre in spacing - favouring the first key
   gives a slow start, favouring the second a fast start and slow arrival.
4. **Add a change of shape**: squash or stretch, a blink, an expression change in the middle.
5. Draw/pose it fully (in CG, key all controls, not only the ones that move).

## Typical breakdown recipes
| Move | Breakdown |
|---|---|
| Head turn | head dips, eyes half-closed or blink, slight tilt |
| Arm wave | elbow leads, wrist bent back (drag) |
| Stand up | hips forward over feet, head down (weight transfer) |
| Look up | chin leads, slight squash before stretch |

## CG notes
- A linear/automatic interpolation gives a 50 % breakdown - always add a breakdown key by hand.
- Tween sliders (Maya tweenMachine; Blender Pose Mode Breakdowner, Shift+E) give a quick
  favoured blend; treat it as a starting point and then change the pose.

## Failure modes
- Breakdown exactly between keys in pose and spacing: robotic.
- Breakdown that moves every part at the same rate: no overlap.
- Breaking the arc to get the shape: keep the path clean.

## Verify
- [ ] Overlay keys + breakdown: the breakdown is visibly off the straight line between keys.
- [ ] One part leads and another drags in the breakdown.
- [ ] Spacing of the breakdown is deliberate (not 50 %).

Related: `creative-arts.animation.principles.keys-extremes-breakdowns`,
`creative-arts.animation.principles.successive-breaking-of-joints`.
