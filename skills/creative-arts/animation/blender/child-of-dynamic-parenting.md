---
id: creative-arts.animation.blender.child-of-dynamic-parenting
name: child-of-dynamic-parenting
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, child-of-set-inverse, set-inverse, dynamic-parenting, constraint-influence, constraint-order, disable-and-keep-transform, prop-handoff]
level: practitioner
status: docs-checked
description: "Hand props between hands and the world in Blender with Child Of: Set/Clear Inverse, keyed influence, Disable and Keep Transform, and constraint stack order."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/child_of.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/interface/header.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/interface/common.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/interface/stack.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# child-of-dynamic-parenting

Goal: a cup picked up from a table, held, passed to the other hand, and put down — without the prop jumping.

## Child Of essentials

- Target (object or bone) with Location, Rotation and Scale axis toggles. The constraint has an animatable Influence, which allows switching parents over time or mixing several Child Of constraints.
- **Set Inverse**: if the child is right with the constraint disabled but wrong with it enabled, this button fixes it. **Clear Inverse**: tells the constraint that the child's current transform with the constraint disabled is its correct relative transform; once enabled, that transform is applied as an offset to the parent.
- The manual notes that Child Of is not suited to chains of bones and cannot emulate connected bones.

## Hand-off workflow (one constraint per parent)

1. Prop has Child Of `hand.R` (influence 0) and Child Of `hand.L` (influence 0); world-space keys on the prop itself.
2. At pickup frame: with hand.R constraint active, **Set Inverse**, key influence 0 on the previous frame and 1 on this frame (constant interpolation).
3. At release, use the header Extras menu **Disable and Keep Transform**: the result is applied to the prop's own transform and the constraint's Influence is set to 0. Key the prop's transform and influence at the switch frame.
4. Repeat for hand.L at the transfer frame: Set Inverse there, influence keyed 0→1 and hand.R 1→0 on the same frame.

## Constraint influence and order

- **Influence** can be keyframed, so constraints can be turned on and off during an animation. Influence 0 is the same as disabling the constraint, and unlike the Enabled toggle it can be animated.
- The stack is evaluated top to bottom; reorder by dragging the grip handle or with Move to First/Last in the header Extras menu.
- **Apply** (Ctrl-A in the Extras menu) bakes the result into the owner's transform and deletes the constraint; applying one that is not first in the stack ignores the constraints above it.
- **Disable and Keep Transform** applies the result to the owner's transform but, instead of deleting the constraint, sets its Influence to 0. It may not work perfectly if the constraint is not first in the stack.

## Alternatives

- Armature constraint with animated weights (see `armature-constraint`); the manual suggests it when the parents are bones and several are blended.

## Gotchas

- Set Inverse at the wrong moment leaves an offset; redo it while the target is in the pose you want to attach at.

## Verify

Scrub across every switch frame: no pops; render from the first frame (not continuing playback) gives identical results.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Child Of constraint page and the constraint header, influence and stack pages: Set Inverse and Clear Inverse behaviour, Extras menu (Apply Ctrl-A, Copy to Selected, Move to First/Last), Disable and Keep Transform (applies the result and sets Influence to 0, no key inserted), keyframeable Influence, top-to-bottom stack evaluation. Removed unconfirmed remarks on Rigify parent switching and scale shear.

Method: documentation only; no commands were run.
