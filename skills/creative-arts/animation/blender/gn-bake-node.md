---
id: creative-arts.animation.blender.gn-bake-node
name: gn-bake-node
category: creative-arts
field: animation
product: blender
tags: [blender, bake-node, node-tools, node-tool, gn-bake, geometry-nodes, gn, operators, asset-shelf, tool-context, selection-node, bake-path, cache]
level: advanced
status: docs-checked
description: "Geometry Nodes Bake node and Node Tools: freeze heavy branches to disk, bake animated results, and ship node groups as operators in menus and the asset shelf with tool-only nodes."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/operations/bake.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/tools.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-bake-node

Goal: (1) stop re-evaluating heavy node trees by baking a branch; (2) ship node groups as one-click tools for artists.

## Bake node

The Bake node is in the Geometry > Operations section of the node menu. It saves and loads intermediate geometry so part of the tree need not be recomputed.

- **Bake Items**: the Geometry item is the default; drag any socket onto the empty socket (or use the *Bake Items* panel in the sidebar Node tab) to add more. Each item has a *Socket Type*, an *Attribute Domain* and an *Is Attribute* flag (the item is an attribute stored on a geometry, so a field such as a mask survives the bake). Rename items with `Ctrl-LMB` on the socket name.
- **Bake Mode**: *Still* bakes the geometry of the current frame; *Animation* bakes several frames, using the scene frame range unless *Custom Range* (*Start*, *End*) is set.
- **Bake** writes the data to disk or packs it into the .blend. Buttons: Pack/Unpack (unpack options match *Unpack Resources*) and *Delete Geometry Node Bake*.
- **Bake Target**: *Inherit from Modifier* (default), *Packed* (inside the .blend) or *Disk*. *Custom Path* sets a *Bake Path* manually; the same path is used for simulation zones.
- Each input gets a matching pass-through output.

The modifier also has a *Bake* panel (Bake Target, Bake Path) and the *Bake Geometry Node* operator bakes every simulation and bake node in the selected objects' modifiers. When data is baked, the number of baked frames shows above the node.

Constraints from the manual: the .blend must be saved to disk before baking; data written by one Blender version may not be readable by another; the baked format is not an import/export format (volumes are saved as OpenVDB).

Baked geometry that references materials lists them in the sidebar Node tab, *Data-Block References* panel, where the references can be changed after baking (only materials are supported).

Patterns:
- **Heavy base, cheap top:** Bake node after the expensive part; iterate on the rest.
- **Animated bake for rendering:** bake animated procedural geometry so render does not re-evaluate it every frame (see `creative-arts.animation.blender.simulation-nodes`).

## Node Tools

A geometry node group can run as a tool from a menu instead of as a modifier.

1. In the Geometry Node Editor header switch the editor type to *Tool*. A group created there gets *Tool* Usage automatically. To convert a modifier group, enable *Tool* in the sidebar Group tab Usage panel (optionally disable *Modifier*) before switching.
2. Set the supported modes and object types with the popovers in the editor header. For mesh objects, shape keys are not supported and are removed when a tool runs.
3. Tools appear in the 3D Viewport's *Non-Assets* menu. To place one in a menu of your choice, right-click the group name in the editor header, *Mark as Asset*, then move it in the Asset Browser into a catalogue named after the menu; it appears at the end of that menu. Save the file as an asset bundle and copy it into an asset library to reuse it in any file.
4. Extra Group Input sockets become properties in the Adjust Last Operation (redo) panel.

Tool-only nodes (only supported in the Tool context): 3D Cursor, Mouse Position, Viewport Transform, Active Element, Selection, Set Selection, Face Set, Set Face Set. Mouse Position works with the group setting *Wait for Click*, which waits for an `LMB` click before the operator runs. Self Object returns the active object inside a tool.

Not supported in the Tool context: Simulation Zone and Viewer, and the inspection features.

## Gotchas

- A Bake node with nothing baked just evaluates its inputs; check the baked-frame count above the node.
- Delete the bake before changing the bake path so no orphan files are left.
- Render farms: ship the bake folder with the .blend, or pack the bake.
- The Selection node only has meaning in tools run in a context that provides a selection.
- Do not rely on baked data across Blender versions.

## Verify

- Bake node: after *Bake*, the baked-frame count shows above the node; *Delete Geometry Node Bake* removes it.
- Tool: appears under *Non-Assets* or the chosen menu, its exposed inputs appear in the redo panel, and one undo reverts it.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed against the Bake node, Baking and Node-Based Tools pages: Bake Mode (Still, Animation, Custom Range), Bake Target options (Inherit from Modifier, Packed, Disk), Bake Items panel, the tool-only node list, Tool Usage and the Non-Assets menu. Removed unconfirmed claims: version gates, default bake path, per-frame file formats, asset shelf behaviour, Active Camera as a tool-only node, timing overlay and Python operator name. Python API checked: 5.2.

Method: documentation only; no commands were run.
