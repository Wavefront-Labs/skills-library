---
id: creative-arts.animation.principles.layered-animation
name: layered-animation
category: creative-arts
field: animation
product: principles
tags: [animation, pose-to-pose-method, layered-animation, straight-ahead, root-first, hierarchy, cg, cycles, overlap]
level: practitioner
status: draft
description: "Animate in layers from the root outward (hips, spine, head, arms, overlap), when it beats pose-to-pose, and how to combine both in one shot."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layered animation

Goal: build motion part by part down the hierarchy so each layer's timing is clean before the
next is added. Williams presents it as the third way next to straight-ahead and pose-to-pose;
CG made it common because controls are independent.

## When to use it
- Cycles (walks, runs, flying, swimming) where the body path is the foundation.
- Overlapping, flowing actions (tails, tentacles, capes, long hair) driven by a core motion.
- Physical, non-acting moves where weight matters more than poses.
Use pose-to-pose instead for acting shots where storytelling poses must land on specific frames.

## Method
1. **Root/hips** - translate and rotate the centre of mass only. Get the weight and the path right
   (vertical bounce, lateral sway). Play it as a moving box.
2. **Legs/feet** - plant contacts, IK feet locked.
3. **Spine and chest** - offset from the hips (follow 1-3 frames).
4. **Head and neck** - offset again, counter-rotate to stabilise.
5. **Arms** - shoulders, then elbows, then wrists, each offset.
6. **Overlap layer** - hair, tails, clothes, fingers.
7. **Face** last.

## Combining with pose-to-pose
Common feature workflow: pose-to-pose keys for the acting beats, then a layered pass for
overlap and offsets on top of the blocked body. In Maya use animation layers; in Blender use
NLA strips or additive layers (Blender 4.4+ layered actions) so the overlap pass can be muted.

## Failure modes
- Starting with arms or face: a later hip change ruins everything above it.
- Over-offsetting each layer: rubbery, boneless motion.
- Never checking the whole: play the full body after each layer.

## Verify
- [ ] Hips-only playblast reads as the intended weight and path.
- [ ] Each child layer is offset from its parent by a consistent, intentional amount.
- [ ] Muting the overlap layer still leaves a solid performance.

Related: `creative-arts.animation.principles.keys-extremes-breakdowns`,
`creative-arts.animation.principles.offset-keys-in-the-graph-editor`.
