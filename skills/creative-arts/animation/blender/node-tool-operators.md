---
id: creative-arts.animation.blender.node-tool-operators
name: node-tool-operators
category: creative-arts
field: animation
product: blender
tags: [blender, node-tool-operators, execute-node-group, node-tools, geometry-nodes, bpy, keymap]
level: advanced
status: docs-checked
description: "How a Geometry Nodes tool becomes an operator: the Identifier setting, registration errors, Wait for Click, redo-panel inputs, and why not to rely on execute_node_group."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/tools.html
  - https://docs.blender.org/api/current/bpy.ops.geometry.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/geometry/node_group_operator.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# node-tool-operators

Goal: understand how a node tool becomes an operator, so it can be called from menus, keymaps and scripts.

## How tools become operators

In the Blender 5.2 source each tool node group registers its own operator, named by the group's **Identifier** (Geometry Node Editor header, Tool editor type, *Options* popover). The identifier is a unique operator identifier and must pass Blender's operator-name check; the Options popover shows registration errors below the field. A group with no Identifier shows "Missing operator identifier" and is not registered.

The operator is invoked from the menus (see `node-tool-menus`) and has these properties in the source: `inputs` (the group's Group Input sockets), `panels`, and viewport data for tools that read the viewport (for example `region_size` and `viewport_is_perspective`). Group inputs appear in the Adjust Last Operation (redo) panel after the tool runs.

The fixed operator `bpy.ops.geometry.execute_node_group`, which older notes describe, is not listed in the current Python API operator documentation for `bpy.ops.geometry`. Do not rely on it; check the operator name with the Info editor in your version.

## Calling a tool from Python or a keymap

- Run the tool once from its menu and copy the operator call from the Info editor to get the exact identifier and arguments for your version.
- Context matters: a tool acts on the active or selected objects in the current mode, and tools using the mouse or viewport need a 3D Viewport region in context. With *Wait for Click* the tool waits for an `LMB` click first.
- Keymap items and pie menu entries refer to the operator by its identifier; use the same string you set in the Identifier field.

## Gotchas

- Renaming the Identifier breaks keymap entries and scripts that refer to it.
- A tool only runs in the modes and for the object types set in the Modes and Object Types popovers.
- Tool-only nodes are not supported in modifiers; the Viewer node and Simulation Zone are not supported in tools.

## Verify

Run the tool from its menu, copy the call from the Info editor, run it again from the Python Console with the same mode and selection, and compare results.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release) and the Blender 5.2 source (branch blender-v5.2-release; python API 5.2). Confirmed in the 5.2 source (editors/geometry/node_group_operator.cc, space_node.py, rna_nodetree.cc): per-tool operator registration from the Identifier property, the Missing operator identifier error, Wait for Click, operator properties inputs and panels. Checked against the 5.2 Python API listing for bpy.ops.geometry, which does not contain execute_node_group. Removed the unconfirmed operator signature, library arguments, keymap and pie code, and version notes.

Method: documentation only; no commands were run.
