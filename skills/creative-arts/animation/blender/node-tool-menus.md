---
id: creative-arts.animation.blender.node-tool-menus
name: node-tool-menus
category: creative-arts
field: animation
product: blender
tags: [blender, node-tool-menus, tool-catalog, node-tools, geometry-nodes, asset-catalogs]
level: practitioner
status: docs-checked
description: "Put geometry node tools in the right 3D viewport menus: Tool flag, supported modes and types, asset catalogs mapping to header menus, and sharing tools via asset libraries."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/tools.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/catalogs.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/geometry/node_group_operator.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# node-tool-menus

Goal: custom node tools appear where users expect them, for example under the Mesh menu in Edit Mode.

## Make a node group a tool

1. In the Geometry Node Editor header, set the editor type to *Tool* (instead of Modifier). A node group created there gets *Tool* Usage automatically; for an existing modifier group enable *Tool* under Usage in the sidebar Group tab first.
2. Header popovers set where the tool applies: **Object Types** (Mesh, Hair Curves, Grease Pencil, Point Cloud), **Modes** (Object, Edit, Sculpt; Draw for Grease Pencil) and **Options**. In Options, *Wait for Click* waits for an `LMB` click before the operator runs, and **Identifier** is the unique operator identifier of the tool. The source shows the error "Missing operator identifier" when it is empty, and a tool without an identifier is not registered as an operator, so set it.
3. Right-click the node group name in the editor header and choose *Mark as Asset*.

## Menu placement by catalogue

The manual: after marking as an asset the group appears in the Asset Browser under *Unassigned*; move it into a catalogue named after a menu and it appears at the end of that menu.

From the Blender 5.2 source:
- The catalogue path becomes the menu path. Catalogues whose root matches a built-in menu are merged into it instead of creating a new menu. Examples for meshes in Edit Mode: `Select`, `Add`, `Mesh`, `Mesh/Extrude`, `Mesh/Clean Up`, `Mesh/Delete`, `Mesh/Merge`, `Mesh/Normals`, `Mesh/Shading`, `Mesh/Split`, `Mesh/Weights`, `Vertex`, `Edge`, `Face`, `Face/Face Data`, `UV`, `UV/Unwrap`; in Object Mode: `Object`, `Object/Apply`, `Object/Convert`, `Object/Quick Effects`; Sculpt Mode: `Sculpt`, `Mask`, `Face Sets`; curves: `Curves`; point clouds: `Point Cloud`.
- Any other root catalogue name becomes an extra menu.
- Tools with no catalogue are listed in the *Unassigned Node Tools* menu; tool groups from the current file that are not assets are listed there under a *Non-Assets* label.
- Only tools whose modes and object types match the current context are listed.

To reuse a tool in every file, save it in an asset bundle and copy it into an asset library, as described in the manual's Node-Based Tools page.

## Gotchas

- Use the exact spelling of the built-in menu names (for example `Clean Up`, not `Cleanup`) or a new menu is created.
- Tool node groups use tool-only nodes (Selection, Set Selection, Mouse Position and others); these are only supported in the Tool context.
- Simulation zones and the Viewer node are not supported in the Tool context.

## Verify

In Edit Mode on a mesh, the tool shows in the intended menu; it is absent in modes or object types it does not support.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release) and the Blender 5.2 source (branch blender-v5.2-release; python API 5.2). Confirmed on the Node-Based Tools page (Tool context, asset and catalogue behaviour, supported modes and types) and in the 5.2 source (editor header popovers Object Types, Modes, Options; Identifier and Wait for Click; built-in menu names that catalogues merge into; Unassigned Node Tools and Non-Assets). Removed unconfirmed claims about shortcut assignment, Quick Favorites, re-saving libraries and duplicate-name behaviour.

Method: documentation only; no commands were run.
