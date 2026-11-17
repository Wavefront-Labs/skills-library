---
id: creative-arts.animation.blender.viewer-node-attribute
name: viewer-node-attribute
category: creative-arts
field: animation
product: blender
tags: [blender, viewer-node, viewer-node-attribute, viewer-domain, viewer-overlay, geometry-nodes, attribute-inspection]
level: practitioner
status: docs-checked
description: "Debug Geometry Nodes with the Viewer node: connect geometry plus a field, set the viewer domain, read it in the viewport overlay and spreadsheet column, and Ctrl Shift click shortcuts."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/output/viewer.html
  - https://docs.blender.org/manual/en/latest/editors/spreadsheet.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/inspection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# viewer-node-attribute

Goal: see any intermediate geometry and field value inside a node tree without wiring it to the output.

## Connect

- Add the Viewer node (Output section). Plug the **Geometry** socket, which must be first, and optionally a field into a further input; more inputs are added by dragging a socket onto the blank socket or in the node's item properties.
- Shortcut: `Shift-Ctrl-LMB` on any node or socket connects it to the active viewer.
- Viewer shortcuts: `Ctrl-1` to `Ctrl-9` assign the selected viewer a number and `1` to `9` activate it.
- The Viewer node only works in the Modifier context, not in node Tool groups.
- Single-value sockets can show their evaluated value next to the socket without a Viewer; geometry and grids cannot.

## Domain

Node property **Domain**: *Auto* chooses the domain from the connected nodes when possible (otherwise Face Corner for meshes and Point for curves), or set it manually. The field is evaluated on that domain, and attributes are interpolated between domains by averaging.

## Display

- **Viewport overlay**: the *Viewer Node* overlay (3D Viewport Overlays popover) shows the attribute value as a grayscale colour; *Color Opacity* sets its opacity and *Attribute Text* prints the values as text in the viewport. The View menu *Viewer Node* option toggles all viewer visualisations so you can compare with the final result.
- **Spreadsheet**: set *Object Evaluation State* to *Viewer Node* (or click the eye icon in the Viewer node header); *Viewer Data* picks which viewer item is shown, and only the columns of the selected domain appear. The Viewer can be pinned so its data stays visible.

## Patterns

- Debug a Compare node: view its boolean on the mesh to see selection before Delete Geometry.
- Instances: the spreadsheet shows the Instances domain values.

## Gotchas

- Inspection tools show data from the last evaluation; nothing is available if the tree has not been evaluated, and socket values are not logged during rendering.

## Verify

Connect a Position Z field: the overlay gradient changes with height and the spreadsheet column shows the same values.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Viewer node, Spreadsheet, Inspection and 3D Viewport overlays pages: Shift-Ctrl-LMB, number shortcuts, Geometry socket first, Domain Auto fallback, Viewer Node overlay (grayscale, Color Opacity, Attribute Text), Viewer Data, pinning, Modifier-only context. Removed unconfirmed claims: version note, output cycling, colour mapping for booleans and vectors, a Viewer column name, active-modifier rule and memory remark.

Method: documentation only; no commands were run.
