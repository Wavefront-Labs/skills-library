---
id: creative-arts.animation.blender.tool-selection-node
name: tool-selection-node
category: creative-arts
field: animation
product: blender
tags: [blender, tool-selection-node, set-selection, node-tools, geometry-nodes, edit-mode]
level: advanced
status: docs-checked
description: "Read and write edit-mode selection in geometry node tools: Selection input node, Set Selection to change what is selected, domains, and building select tools."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/tools.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/write/set_selection.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# tool-selection-node

Goal: node tools that act only on the selected elements or create new selection patterns (select by angle, random, by attribute).

These nodes are only supported in the Tool context (Geometry Node Editor type *Tool*); see `gn-bake-node` for the tool setup.

## Selection node (input)

The Selection node (Geometry > Read section of the node menu) outputs a boolean field that is true for geometry selected in Edit Mode and false elsewhere. Use it as the *Selection* input of operations (Extrude Mesh, Set Position, Delete Geometry) so the tool only touches selected elements.

## Set Selection (output)

The Set Selection node takes *Geometry*, a boolean *Selection* field and a *Domain* property. Elements for which the field is false are implicitly de-selected in the output geometry, so the selection you set is the complete new selection.

## Example: select faces facing up

```
Group Input.Geometry -> Set Selection (Domain Face, Selection = Compare(Dot Product(Normal, (0,0,1)) > cos(30 degrees))) -> Group Output
```
Mark the tool for Edit Mode and Mesh, and give it a catalogue such as `Select` so it lands in that menu (see `node-tool-menus`).

## Combining with the existing selection

Boolean Math: `Selection AND condition` (refine), `OR` (extend), `NOT` (invert). Because Set Selection de-selects everything the field leaves false, OR with the Selection node to keep the old selection.

## Related tool nodes

Face Set (outputs which face set a face is in, 0 if the mesh has none, plus an *Exists* boolean) and Set Face Set (*Selection*, *Face Set* integer field); 3D Cursor (*Location*, *Rotation*); Viewport Transform (*Projection*, *View*, *Is Orthographic*); Active Element (index of the active element in a chosen domain, plus *Exists*).

## Gotchas

- The Selection node has no inputs and only means something in a tool.
- Set Selection de-selects elements where its field is false.
- Tool shape key support: for mesh objects shape keys are not supported and are removed when a node tool runs.

## Verify

Run the tool on a cube in Edit Mode: only the top face ends up selected; with the refine logic it respects a prior selection.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Selection, Set Selection, Face Set, Set Face Set, 3D Cursor, Viewport Transform, Active Element and Node-Based Tools pages: tool-only restriction, Selection output, Set Selection de-selecting false elements, Domain property, shape key removal. Removed unconfirmed claims: Sculpt mask behaviour, domain flush rules and the list of settable domains.

Method: documentation only; no commands were run.
