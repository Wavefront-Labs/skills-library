---
id: creative-arts.animation.blender.spreadsheet-domains
name: spreadsheet-domains
category: creative-arts
field: animation
product: blender
tags: [blender, spreadsheet, spreadsheet-domains, spreadsheet-domain, attribute-domains, geometry-nodes, attribute-inspection]
level: practitioner
status: docs-checked
description: "Read Blender geometry by attribute domain in the Spreadsheet: Mesh (vertex, edge, face, face corner), Curves (control point, spline), Point Cloud, Instances, Volume grids, GP layers."
sources:
  - https://docs.blender.org/manual/en/latest/editors/spreadsheet.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# spreadsheet-domains

Goal: find the attribute you are debugging by looking in the right component and domain.

## Left region: data set tree

The left region (Data Set) has a *Geometry* list for browsing nested geometry (for example a mesh inside an instance) and a *Domain* list; the number of elements in each domain is shown next to its entry.

- **Mesh**: *Vertex* (position, custom point attributes), *Edge* (`sharp_edge`, `crease_edge`, `uv_seam`), *Face* (`material_index`, `sharp_face`), *Face Corner* (UV maps and other corner attributes).
- **Curves**: *Control Point* (`position`, `radius`, `handle_left`, `handle_right` on Bezier curves), *Spline* (`resolution`, `cyclic`).
- **Point Cloud**: *Point*.
- **Instances**: one row per instance.
- **Volume**: shows per-grid information (grid name, data type, class, voxel extent, minimum voxel, voxel and tile counts, size), not voxel values.
- **Grease Pencil**: attributes can live on the *Layer* domain.

Element counts beside each entry are a fast way to compare geometry before and after a node.

## Reading the table

- Each column is an attribute or data property; each row is an element (vertex, face, spline, instance and so on). Column names and row indices stay visible while scrolling.
- Built-in attribute names follow the attribute reference: `position`, `sharp_face`, `material_index`.
- Attributes whose names start with a period are internal; show them with View menu, *Internal Attributes*.
- Tooltips give more detail; for example Byte Color is displayed as scene linear floats with the real integer values on hover, and Matrix values appear only in tooltips.

## Domain gotchas

- An attribute stored on Face Corner won't appear under Vertex — Geometry Nodes *Store Named Attribute* domain decides where it lives.
- Attributes are interpolated automatically between domains in nodes, normally by averaging; the Spreadsheet shows the domain you select.
- To filter on an attribute of another domain, copy it to the current domain with Store Named Attribute and filter on the copy.

## Verify

Store a test attribute on Face, then check it appears only under *Face* with the expected count.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Spreadsheet and Attributes Reference pages: Geometry and Domain lists with element counts, volume grid statistics, Internal Attributes toggle, tooltip behaviour, built-in attribute names and domains. Removed unconfirmed claims: version notes, tilt and curve_type attributes, `.select_vert`, the seams attribute name (the documented name is uv_seam) and the Face Corner count remark.

Method: documentation only; no commands were run.
