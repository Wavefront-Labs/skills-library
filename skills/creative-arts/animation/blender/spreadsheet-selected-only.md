---
id: creative-arts.animation.blender.spreadsheet-selected-only
name: spreadsheet-selected-only
category: creative-arts
field: animation
product: blender
tags: [blender, spreadsheet, spreadsheet-selected-only, selected-only-filter, edit-mode, attribute-inspection, pinning]
level: practitioner
status: docs-checked
description: "Inspect only what you selected in Blender's Spreadsheet: Selected Only filter in Edit mode, pinning an object, and matching viewport selection to rows when debugging geometry."
sources:
  - https://docs.blender.org/manual/en/latest/editors/spreadsheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spreadsheet-selected-only

Goal: read exact values (position, UVs, weights) of a handful of selected elements on a dense mesh.

## Selected Only

- Header toggle **Show Only Selected**: only available when the object is in Edit Mode; when checked, only data for the selected geometry elements is shown.
- Use the left-region *Domain* list to match the selection mode (vertex select, Vertex domain).

## Pinning

- The Spreadsheet shows the active object. In the *Context Path* panel, clicking the pin (unpinned) icon locks it to the current active object and data path so you can select other objects; click again to unlock.
- The Context Path panel header shows the object name, and arrows between names let you hide the modifier.

## Typical uses

- Check symmetry: select two mirrored vertices and compare their `position` values.
- Narrow a search for a bad value: combine Show Only Selected with a row filter (see `spreadsheet-row-filters`).

## Gotchas

- Show Only Selected is only available in Edit Mode.
- The Object Evaluation State (Evaluated, Original, Viewer Node) decides which data is shown; see `spreadsheet-evaluation-state`.

## Verify

Select 3 vertices: the status bar shows the reduced row count.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Spreadsheet page: Show Only Selected (Edit Mode only), Context Path pin behaviour, Domain list, status bar counts. Removed unconfirmed claims about the icon, evaluated-selection mapping, performance remarks, shape key behaviour and Select All by Trait use.

Method: documentation only; no commands were run.
