---
id: creative-arts.animation.blender.freestyle-line-set-selection
name: freestyle-line-set-selection
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-line-set-selection, freestyle-edge-types, freestyle-visibility, freestyle, line-sets, npr]
level: practitioner
status: docs-checked
description: "Choose which edges Freestyle draws: line set selection by visibility, edge types, face marks, collections and image border, crease angle and multiple line sets."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_set.html
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/freestyle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# freestyle-line-set-selection

Goal: draw exactly the outlines you want (silhouettes heavy, interior creases light, hidden lines dashed) by combining line sets.

## Line set selection (View Layer Properties → Freestyle Line Set)

- **Select By → Image Border**: only geometry inside the image border is considered; cuts render time but can cause continuity problems when geometry moves in and out of view.
- **Visibility**: *Visible* (occluded by no surface), *Hidden* (occluded by at least one surface) or *Quantitative Invisibility* with *Start*/*End* (range of occluding surfaces).
- **Edge Types**: Silhouette, Crease, Border (open mesh edges), Edge Mark, Contour, External Contour, Material Boundary, Suggestive Contour, Ridge & Valley. At least one must be chosen to get output; several can combine, and the *X* next to a type excludes it.
- **Face Marks**: faces marked in Edit Mode (`Ctrl F`, Face Data → Mark Freestyle Face) with *Negation* (include/exclude) and *Condition* (*One Face* or *Both Faces*).
- **Collection**: *Line Set Collection* plus *Negation* to include or exclude objects by collection.

## Crease and edge marks

- *View Layer → Freestyle → Crease Angle* drives *Crease* edge selection and also affects *Silhouette* selection.
- Mark edges in Edit Mode with `Ctrl E` → *Mark Freestyle Edge* (stored as the `freestyle_edge` attribute), then enable *Edge Mark* in the line set. Face marks are stored as `freestyle_face`.
- *Suggestive Contour* and *Ridge & Valley* depend on the view map *Sphere Radius* (and *Kr Derivative Epsilon* for suggestive contours).

## Multiple line sets

A view map (one per view layer) can have several line sets, each linked to one line style. Typical setup:
1. `Outline`: Silhouette + External Contour + Border, visible, thick style.
2. `Detail`: Crease + Edge Mark, visible, thin style.
3. `Hidden`: Silhouette + Crease with Hidden visibility, thin dashed style.

## Gotchas

- Silhouette cannot render open meshes such as planes or open cylinders; use Border or Crease for those.
- *Culling* in the view map ignores out-of-view edges, which saves time and memory but may reduce quality.

## Verify

Render with one line set at a time and confirm each draws only its intended edges.

## Checked

2026-10-27 against the Blender 5.2 manual (Freestyle Line Set and View Layer Freestyle pages). Confirmed panel names, visibility types, edge type list, edge and face marks and shortcuts, collection and image border options. Removed the unconfirmed crease angle default, QI numeric examples, logical AND/OR options and the flipped-normals and slow-edge-type claims.
Method: documentation only; no commands were run.
