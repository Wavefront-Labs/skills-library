---
id: creative-arts.animation.vector-graphics.harmony-pegs-and-hierarchy
name: harmony-pegs-and-hierarchy
category: creative-arts
field: animation
product: vector-graphics
tags: [harmony-pegs, pegs, hierarchy, parenting, pivots, toon-boom-harmony, cut-out-rig]
level: advanced
status: draft
description: "Set up pegs and a parent-child hierarchy in Harmony: pivot placement, hip-to-hand chains, peg versus drawing transforms, 2D versus 3D pegs and animating on pegs."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pegs and hierarchy (Toon Boom Harmony)

A **peg** is a node that applies a transformation to everything connected below it. Chaining pegs gives a parent-child hierarchy: rotate the upper arm peg and the forearm and hand follow.

## Building the chain
1. Plan the hierarchy as a tree: hips (or torso) at the root; spine, chest, neck, head, then limb chains (upper arm > forearm > hand).
2. For each part make a Peg and connect the Drawing node below it. Connect the child's peg under the parent's peg (peg to peg) so that the hierarchy passes the transformation down (`harmony-node-view-for-cut-out-rigs.md`).
3. **Set pivots** at joints: with the peg selected, use the Rotate tool in the Camera view and move its pivot to the shoulder, elbow, wrist, hip and so on. Do this before animating: moving a pivot later shifts the part.
4. Animate rotation on the peg (not on the drawing), with the Transform tool; use the Animate mode with keyframes in the Timeline or Camera view.
5. Add a master peg above everything for global positions.

## 2D and 3D pegs
- Pegs can work in 2D or enable 3D, allowing Z depth and rotation in 3D space; this matters with the multiplane camera. Mixing the two types in a chain needs care; the docs describe how the 3D option is controlled.

## Practical tips
- Keep drawings on top of pegs only for part-specific adjustments such as shape offsets; the pegs hold the motion.
- Copy a peg hierarchy as a template to reuse for multiple characters of the same build.
- Use the Timeline to see which pegs are animated; clean unused keyframes to keep the scene readable.

## Verify
- [ ] Rotating a parent peg moves all children as expected.
- [ ] Pivots sit on anatomical joints.
- [ ] No transformations are baked into drawings that should be on pegs.
