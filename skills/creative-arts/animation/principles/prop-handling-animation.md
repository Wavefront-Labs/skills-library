---
id: creative-arts.animation.principles.prop-handling-animation
name: prop-handling-animation
category: creative-arts
field: animation
product: principles
tags: [animation, secondary-action-principle, prop-handling-animation, props, contact, grip, weight, constraints, child-of, parent-switch, cg]
level: practitioner
status: draft
description: "Animate characters handling props: believable grip and contact, prop weight in the body, and clean pick-up/put-down hand-offs with constraints in CG."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/child_of.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prop handling animation

Goal: props feel physically held and used, and their handling expresses character.

## Contact and grip
- Fingers wrap around the prop's real form; no gaps or interpenetration at contact points.
- Thumb opposition: most grips have the thumb opposite the fingers.
- Grip strength shows in tension: a tight fist on a weapon, loose fingertips on a teacup.
- The prop is **not** glued to the palm centre: hold position follows how that object is held
  (pen near fingertips, hammer at the handle end).

## Weight
- A heavy prop changes the whole body: lean opposite to counterbalance, slower lifts,
  shoulders drop on the holding side.
- Light props move with the hand's overlap: a lifted cup lags slightly and settles.

## Pick-up and put-down (CG)
1. Animate the hand reaching (eyes lead, wrist leads).
2. On the contact frame, switch the prop's parent from world to hand. Blender: Child Of
   constraint with influence keyed 0->1 and "Set Inverse" at the contact frame, or a
   parent-switch rig; Maya: parent constraint with keyed weights or a space-switch control.
3. Key the prop on the frame before the switch at its world position so it does not jump.
4. On release, reverse: key the world space position, switch parent, let gravity settle the prop.
5. Check the contact frames in stepped playback for pops.

## Character through handling
- Fidgeting with a prop reveals nerves; precise handling shows competence; dropping or
  fumbling is comedy.
- Use the prop as a secondary action that underlines the line reading.

## Failure modes
- Prop sliding in the hand during the hold (constraint not keyed correctly).
- Hand passing through prop geometry.
- No weight response to a heavy object.

## Verify
- [ ] No prop pop on pick-up/put-down frames.
- [ ] Contact points stay locked during the hold.
- [ ] Body reacts to prop weight proportionally.

Related: `creative-arts.animation.principles.secondary-action-hierarchy`,
`creative-arts.animation.principles.heavy-lift`.
