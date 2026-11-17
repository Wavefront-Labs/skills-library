---
id: creative-arts.animation.vector-graphics.harmony-node-view-for-cut-out-rigs
name: harmony-node-view-for-cut-out-rigs
category: creative-arts
field: animation
product: vector-graphics
tags: [harmony-node-view, node-view, toon-boom-harmony, cut-out-rig, composite, nodes, rigging]
level: advanced
status: draft
description: "Build a cut-out rig network in Toon Boom Harmony's Node view: Read, Peg and Composite nodes, grouping, naming, hierarchy order and common mistakes."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Node view network for a cut-out rig (Toon Boom Harmony)

Harmony scenes are node graphs: the timeline is only one view of them. A cut-out puppet is built from nodes in the Node view, which makes the hierarchy visible and editable. Edition features differ, so check the Harmony documentation for what your edition includes.

## Node types you use
- **Drawing (Read) node**: a drawing layer with its timing columns.
- **Peg node**: a transformation node (position, rotation, scale, skew), used to move and parent parts (`harmony-pegs-and-hierarchy.md`).
- **Composite node**: merges its inputs into one image; the Composite connects to the scene's Display and Write nodes.
- **Group node**: wraps several nodes into one tidy unit (for a character or a body part). The inside can contain its own composite, pegs and deformers.
- **Deformation nodes**: bone and curve deformers (`harmony-bone-and-curve-deformers.md`).
- **Cutter, Colour-Override, Blur, Glow** and other effect nodes, for compositing.

## Structure that works
1. Create a Group per character, with Drawing nodes for each body part inside.
2. Each part connects through a Peg to a Composite. Stacking order of the Composite inputs sets which part is in front; use Z values on pegs for depth rather than relying on the order alone.
3. Name nodes clearly (`L_forearm_drw`, `L_forearm_peg`) with a convention, since you will script and search by name (`harmony-qtscript-scene-scripting.md`).
4. Keep a Master Peg at the top of the group to move the whole character.
5. Make pivots explicit: set the pivot for each peg at the joint.

## Mistakes to avoid
- Applying rotation to the drawing's own transformation rather than to a peg.
- Creating loops or branches that bypass the composite, so the part does not render.
- Leaving unnamed nodes, which become unmanageable in large rigs.
- Editing templates in many places rather than in the master (use the Library for reuse, `harmony-drawing-substitution-and-libraries.md`).

## Verify
- [ ] Every part reaches the Composite through a peg.
- [ ] Naming is consistent, and group nesting is shallow.
- [ ] Moving the Master Peg moves the whole puppet.
