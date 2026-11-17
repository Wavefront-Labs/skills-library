---
id: creative-arts.animation.blender.spreadsheet-row-filters
name: spreadsheet-row-filters
category: creative-arts
field: animation
product: blender
tags: [blender, spreadsheet, spreadsheet-row-filters, row-filter, attribute-inspection, debugging, geometry-nodes]
level: practitioner
status: docs-checked
description: "Filter Blender Spreadsheet rows by attribute value: column name, operation (equal, greater, less), threshold for floats, vector and boolean filters, combining filters to find bad data."
sources:
  - https://docs.blender.org/manual/en/latest/editors/spreadsheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spreadsheet-row-filters

Goal: answer "which elements have this value" without scrolling a million rows.

## Adding filters (Spreadsheet Sidebar, `N`)

- Click **Add Row Filter** in the Sidebar; set the **Column** name of an existing column (for example `position`, `material_index`, `radius`). If no column has that name the filter is grayed out and ignored.
- **Operation**: for numerical columns *Equal To*, *Greater Than*, *Less Than*; other columns only support *Equal To*.
- **Value** is the comparison value; **Threshold** is how far a row may deviate from the value before it is excluded (Equal To uses it).
- Each filter has an **Enabled** checkbox; the header **Use Filter** toggle turns all filters on or off. The status bar shows the row and column counts and how many rows remain after filtering.

## Recipes

- Out-of-range material: `material_index` Greater Than (number of slots minus 1).
- Points below ground: store a boolean attribute in Geometry Nodes (for example from a Compare on position Z) and filter on that column.
- Zero-radius points: `radius` Equal To 0 with a small threshold.

## Gotchas

- The column must exist on the current domain; for an attribute on another domain, copy it to this domain with Store Named Attribute and filter on the copy.
- Filters persist in the editor; forgetting an enabled one makes data seem to disappear, so check the status bar row count.
- For complex conditions compute a boolean in Geometry Nodes, preview with the Viewer node, filter on that.

## Verify

Turn off *Use Filter*: the total row count returns; turn it back on and toggle filters one at a time.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Spreadsheet page: Add Row Filter in the Sidebar, Enabled, Column (grayed out when missing), Operation (numerical columns only for Greater/Less), Value, Threshold, Use Filter header toggle, status bar counts, Store Named Attribute workaround. Removed unconfirmed claims: case sensitivity, vector component-wise comparison, filter combination logic and the specific threshold numbers.

Method: documentation only; no commands were run.
