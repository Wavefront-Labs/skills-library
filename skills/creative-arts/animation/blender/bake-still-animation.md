---
id: creative-arts.animation.blender.bake-still-animation
name: bake-still-animation
category: creative-arts
field: animation
product: blender
tags: [blender, bake-still-animation, bake-still, bake-animation-mode, bake-node, geometry-nodes, gn-bake]
level: practitioner
status: docs-checked
description: "Use the geometry nodes Bake node in Still or Animation mode: caching expensive results, bake items, custom frame range, packed or disk target, and deleting a bake."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/operations/bake.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# bake-still-animation

Goal: freeze the expensive part of a node tree so the rest stays interactive.

## Bake node basics

The Bake node saves and loads intermediate geometry, baking part of the node tree for better performance. The default bake item is Geometry; more items are added by dragging sockets into the blank socket or in the Sidebar > Node > **Bake Items** panel (each item has a socket type, attribute domain and Is Attribute option). Each input gets a matching pass-through output. Some properties are only editable in Sidebar > Node > Properties.

## Modes (Bake Mode)

- **Animation**: bakes the geometry data for multiple frames. By default the scene frame range is used, or define a **Custom Range** (Start, End). Use for animated upstream data.
- **Still**: bakes the geometry data of the current frame. Use for heavy static work.

## Workflow

1. Place the Bake node right after the expensive section.
2. Choose the mode, the **Bake Target** (Inherit from Modifier is the default, or Packed, or Disk), and a **Custom Path** if needed (the bake path is also used for simulation zones). See `creative-arts.animation.blender.bake-path-packed`.
3. Press **Bake**. Pack/Unpack and Delete Geometry Node Bake appear next to it. Downstream nodes keep evaluating on the baked data.
4. The blend-file must be saved before data can be baked. Data is not stored until the Bake operation is run. The Bake Geometry Node operator bakes the simulations and bake nodes in all modifiers of the selected objects.

## Gotchas

- Baking a Still of animated input freezes that animation at the baked frame: wrong mode is the usual cause of "my animation stopped".
- The baked format is not an import/export format, and data written by one Blender version may not be readable by another (manual warning). Volumes are saved as OpenVDB.
- Remove attributes you do not need downstream before the Bake node to keep the bake small.
- After a bake, the number of baked frames is shown above the Bake node (or simulation zone).

## Verify

After baking, the frame count shows on the node, Animation mode scrubs smoothly, and Still mode shows the same result on every frame.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Bake Items panel, Bake Mode values, Custom Range, Bake Target values and default, Custom Path, Pack/Unpack and Delete Geometry Node Bake, saved-file requirement, version compatibility warning, baked-frames display.
Removed as unconfirmed: the "4.1+" version gate, the Shift A menu path, the claim that baked data keeps being used when upstream nodes change, and the Node Timings overlay verification.
Method: documentation only; no commands were run.
