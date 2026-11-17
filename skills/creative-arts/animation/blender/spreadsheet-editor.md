---
id: creative-arts.animation.blender.spreadsheet-editor
name: spreadsheet-editor
category: creative-arts
field: animation
product: blender
tags: [blender, spreadsheet, attribute-inspection, viewer-node, attributes, geometry-nodes, debugging, named-attributes, domains, instances, volume-grids]
level: practitioner
status: docs-checked
description: "Use Blender's Spreadsheet editor and Viewer node to inspect geometry attributes by domain, debug Geometry Nodes fields and read element counts."
sources:
  - https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/spreadsheet.rst
  - https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/geometry_nodes/output/viewer.rst
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# spreadsheet-editor

Goal: see the actual numbers behind geometry, which is the way to debug a Geometry Nodes field or a mystery attribute.

## Data set (left region)

- **Object Evaluation State**: *Evaluated* (modifiers applied), *Original* (no modifiers) or *Viewer Node* (data from the active Viewer node). Compare Original and Evaluated to see what a modifier changed.
- **Context Path** shows the active object and lets you hide modifiers in the path; the pin toggle locks the editor to the current object and data path, so selecting something else does not change the table.
- **Geometry** browses nested geometry, for example a mesh inside an instance or a geometry collection.
- **Domain** picks the attribute domain (vertices, faces, splines, instances and so on) and shows the element count of each.
- Volume components list their **Volume Grids** with name, data type, class, voxel extent, min voxel, voxel counts, tiles and size.

## Table

- One column per attribute or data property. Byte Color values display as scene-linear floats; hover to see the underlying integers. Matrix values appear only in tooltips.
- Attributes whose names start with a period are internal; show them with *Internal Attributes* in the View menu.
- *Show Only Selected* (header) works in Edit Mode only and limits rows to selected elements.
- **Row Filter** (sidebar): *Add Row Filter*, each with Enabled, Column, Operation, Value and Threshold. Numeric columns offer Equal To, Greater Than and Less Than; other columns only Equal To. Threshold is how far a value may deviate before the row is excluded. The header *Use Filter* toggle switches filters on and off, and the status bar shows how many rows remain.

## Viewer node

- Connect any node or socket to the active viewer with `Shift Ctrl LMB`.
- Give a viewer a number with `Ctrl 1`, `Ctrl 2` and so on (shown at its upper right); activate it later with the number keys `1` to `9` (only those keys).
- The viewer's **Domain** sets the domain used to evaluate its Value input. *Auto* picks it from the connected nodes; if Auto cannot decide, meshes use Face Corner and curves use Point.
- With a Geometry input and a field input both connected, the field values can be drawn in the 3D Viewport through the Viewer overlay. The Geometry socket must be first.
- In the spreadsheet, *Viewer Path* shows the route from the modifier to the active viewer (through group nodes) and *Viewer Data* picks which item to show when a viewer outputs several. Switch between Evaluated and Viewer Node by clicking the viewer node's header icon. A pinned viewer keeps its data visible when the active object or node selection changes.
- The spreadsheet shows only attribute columns that match the selected domain.

## Verify

- The attribute you expect appears on the expected domain in Evaluated state.
- The viewer's column changes when you change a node parameter.
- Row counts match your expectation after a merge, delete or realize step.

## Checked

2026-11-01. Confirmed against the Blender manual pages for the Spreadsheet editor and the Viewer node (sources above): data set options, domains and counts, volume grid fields, Show Only Selected, Row Filter fields and operations, internal attributes menu item, Byte Color display, viewer shortcuts, Auto domain fallback, pinning, geometry socket order. Removed as not stated on those pages: the per-version notes, the list of built-in attribute names, the full column type list, the Python snippet, the export and glTF colour remarks, and the gotchas list.
Method: documentation only; no commands were run.
