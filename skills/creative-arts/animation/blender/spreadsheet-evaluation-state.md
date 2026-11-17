---
id: creative-arts.animation.blender.spreadsheet-evaluation-state
name: spreadsheet-evaluation-state
category: creative-arts
field: animation
product: blender
tags: [blender, spreadsheet, spreadsheet-evaluation-state, evaluated-data, original-data, viewer-node, modifier-stack]
level: practitioner
status: docs-checked
description: "Choose what Blender's Spreadsheet shows: Evaluated (after modifiers), Original (mesh data), or Viewer Node output — and how this explains 'my attribute is missing' bugs."
sources:
  - https://docs.blender.org/manual/en/latest/editors/spreadsheet.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/output/viewer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spreadsheet-evaluation-state

Goal: know whether you are looking at the base mesh, the final modified result, or an intermediate node.

## Object Evaluation State (Data Set region, left side)

- **Evaluated**: data with all modifiers applied.
- **Original**: the object's data without modifiers.
- **Viewer Node**: data from the active Viewer node. `Shift-Ctrl-LMB` on a node or socket connects it to the active viewer. You can also toggle between Evaluated and Viewer Node with the eye icon in the Viewer node's header. In this state the panel also shows a *Viewer Path* (modifier to viewer, through any node groups) and *Viewer Data* (which Viewer item to display when the Viewer has several).

## Debugging pattern

1. Attribute missing in Evaluated → check Original: did it ever exist?
2. Exists in Original but not Evaluated → something in the stack dropped or changed it (anonymous attributes are not propagated by simulation zones unless stored, for instance). Move the step earlier or store the attribute under a name.
3. Exists in GN but not after → later modifiers or a *Remove Named Attribute*; use Viewer at each stage.
4. Evaluated count differs from Original → a modifier or node changed the element count; expected.

## Notes

- The Spreadsheet inspects the active object; the pin icon in the *Context Path* panel locks it to the current object and data path.
- Clicking the arrows between names in the Context Path hides the modifier.
- Instance data appears under the *Instances* domain; use the *Geometry* list to browse nested geometry.
- The Viewer node cannot be used in the Tool context, only in the Modifier context.

## Verify

Add a modifier that changes the vertex count (for example Subdivision Surface): the Vertex count differs between Original and Evaluated.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Spreadsheet, Viewer node and Simulation Zone pages: Object Evaluation State options, Viewer Path and Viewer Data, Shift-Ctrl-LMB, eye icon toggle, Context Path pin, Tool context restriction. Removed unconfirmed claims: Node Wrangler dependency, which modifiers drop attributes, Edit-mode toggle interactions and the exact 8 and 26 vertex counts.

Method: documentation only; no commands were run.
