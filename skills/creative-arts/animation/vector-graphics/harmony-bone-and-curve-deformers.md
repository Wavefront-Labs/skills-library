---
id: creative-arts.animation.vector-graphics.harmony-bone-and-curve-deformers
name: harmony-bone-and-curve-deformers
category: creative-arts
field: animation
product: vector-graphics
tags: [harmony-deformers, deformers, bone-deformer, curve-deformer, toon-boom-harmony, cut-out-rig]
level: advanced
status: draft
description: "Rig organic bends in Harmony with bone and curve deformers: when to use each, setup order, rest pose, influence and deformation chains and avoiding stretching artefacts."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Bone and curve deformers (Toon Boom Harmony)

Pegs rotate rigid parts. For bendy limbs, tails, hair or cloth, Harmony has deformers, which bend a drawing along a skeleton or curve. Deformation tools are part of the cut-out toolset; check the documentation for edition availability.

## Kinds
- **Bone deformer**: a chain of bones that rotates and bends the vector drawing; good for arms, legs and spines.
- **Curve deformer**: control points along a bezier; good for tails, tentacles, hair and flexible tubes.
- Deformers also exist as other types (for example, free-form/envelope style); consult the Harmony docs for the list in your version.

## Setup order
1. Draw the part in a neutral, straightened **rest pose**. Deformers are built on this pose.
2. With the drawing in the Camera view, use the Deformation tools or the Create Deformation command to lay down the chain along the part.
3. Name the deformer's nodes and keep them in the group.
4. Adjust the **influence** (how far each bone affects the artwork) so that bends are smooth at the joint.
5. Add a **deformation chain** to attach several deformers end to end (upper arm bone, then forearm bone).
6. Animate by rotating the bones or moving the curve control points in the Camera view.

## Pitfalls
- Skipping the rest-pose step makes later edits look wrong.
- Extreme bends cause pinching or stretching; split the part and use a peg for a rigid hinge where a bend is unrealistic.
- Mixing pegs and deformers on the same part leads to double transformations; decide which controls the part.
- Keep drawing shapes simple: fewer points deform more cleanly (`pen-tool-and-bezier-handle-discipline.md`).

## Verify
- [ ] Bend each joint through its range, check for pinch or tearing.
- [ ] Rest pose returns the artwork to its original shape.
