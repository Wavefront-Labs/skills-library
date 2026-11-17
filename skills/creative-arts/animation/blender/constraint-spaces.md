---
id: creative-arts.animation.blender.constraint-spaces
name: constraint-spaces
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, constraint-spaces, owner-space, target-space, pose-space, local-space, custom-space]
level: practitioner
status: docs-checked
description: "Pick the right owner/target space for Blender constraints: World, Custom, Pose, Local, Local with Parent and Local (Owner Orientation), and what each is for."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/interface/common.html#space
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/transformation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# constraint-spaces

Goal: understand why the "same" constraint behaves differently and choose spaces deliberately.

## Spaces

Target Space is the frame in which the target's location, rotation and scale are read; Owner Space is the frame in which they are applied.

- **World Space**: relative to the world axes.
- **Custom Space**: relative to an arbitrary object or bone, for example a vehicle or a character root. With Limit Distance, evaluating both owner and target in a Custom Space scales the Distance with that space's object or bone.
- **Pose Space** (bones only): relative to the armature object.
- **Local Space**: for an object, relative to its parent; for a bone, relative to its rest state after that rest state was transformed by the bone's ancestors (with no other constraints this is what the Properties editor shows in Pose Mode). For objects without a parent it has a legacy meaning that may be removed; use World Space instead.
- **Local with Parent** (bones only): relative to the bone's rest state, including the rotation and location difference caused by rotating any ancestor bone.
- **Local Space (Owner Orientation)** (bone targets only): meant for use with the Owner set to Local Space. It takes the target bone's Local Space adjusted to the owner bone's rest orientation, so with both parents in rest pose the owner undergoes the same transformation as the target in armature space.

## Rules of thumb

- Copy a control's animation channels to another bone: Local to Local; use Local Space (Owner Orientation) on the target when the two bones have different rest orientations.
- Stick to a world position: World to World.
- Transformation and Action constraint inputs: pick a target space that stays stable when parents move, usually Local.

## Debug procedure

1. Set influence 1, move only the target; watch the owner.
2. Swap target space between World/Pose/Local and note which matches intent.
3. Check bone roll (armature Axes display) — local axes differences cause sideways motion.

## Gotchas

- Objects have no Pose Space, Local with Parent or Owner Orientation: those are for bones (the last for bone targets).
- Check bone roll (armature Axes display); different local axes cause sideways motion in Local to Local copies.

## Verify

The owner follows only the intended movement when the armature object itself is moved/rotated (Pose/Local spaces stay correct; World changes).

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the constraint Space page: the definitions of World, Custom, Pose, Local, Local with Parent and Local Space (Owner Orientation), which are bone-only, the legacy meaning of Local Space for parentless objects, and the Custom Space tip on Limit Distance. Removed the unconfirmed 2.9+ version gate, the claim that Local Space ignores constraints on the target, and the Pose to Pose rule.

Method: documentation only; no commands were run.
