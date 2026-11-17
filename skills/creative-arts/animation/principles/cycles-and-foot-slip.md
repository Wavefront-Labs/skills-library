---
id: creative-arts.animation.principles.cycles-and-foot-slip
name: cycles-and-foot-slip
category: creative-arts
field: animation
product: principles
tags: [animation, walk-cycle, foot-slip, in-place-cycle, progressive-walk, root-motion, treadmill, cycles, game-animation, ik]
level: practitioner
status: draft
description: "Choose in-place vs progressive walks, compute ground speed so planted feet do not slip, and handle root motion for games and long camera tracks."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cycles and foot slip

Goal: walks and runs whose planted feet stick to the ground, whether animated in place,
progressively across a set, or as game root motion.

## In-place (treadmill) cycle
- The body stays at the origin; planted feet slide backward at constant speed.
- Ground speed (units per frame) = stride length / frames per step. Planted foot must move back
  exactly that much each frame - use linear interpolation on the planted foot's forward channel.
- Later, the whole character (or the background) moves forward at the same speed.

## Progressive walk
- Feet stay fixed in world space while planted; the body moves forward.
- Easiest for acting walks that change speed or path. Key feet in world space with IK, hold
  them with constant/flat keys during contact.

## Converting a cycle to progressive
1. Make curves cyclic (Blender: Cycles modifier; Maya: Cycle with Offset on the forward channel
   so each cycle continues forward).
2. Animate a parent/root moving forward at ground speed, linear.
3. Scrub contact frames: if the planted foot drifts, the root speed or stride does not match.

## Games: root motion
- Either export in-place with a separate velocity (engine moves the capsule), or bake forward
  motion into the root bone (root motion) so the engine reads it. Root speed must match stride
  exactly or feet slide at runtime.
- Loop must start and end on the same pose; delete the duplicate last frame on export.

## Failure modes
- Slight foot slide from mismatched speed (most common walk note).
- Cycle that does not loop: last frame duplicates the first and causes a hitch.
- Root bobbing up and down in root motion (put bounce on the hips, not the root).

## Verify
- [ ] Planted foot stays within a pixel (or a few mm) during contact.
- [ ] Cycle loops with no hitch.
- [ ] Ground speed = stride / frames per step.

Related: `creative-arts.animation.principles.walk-timing`,
`creative-arts.animation.principles.offset-keys-in-the-graph-editor`.
