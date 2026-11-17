---
id: creative-arts.animation.blender.merge-vertices
name: merge-vertices
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, merge-vertices, merge-at-center, collapse, merge-by-distance, auto-merge, weld]
level: practitioner
status: docs-checked
description: "Merge vertices in Blender (M): At Center, Cursor, First, Last, Collapse and By Distance (with Sharp Edges option), plus Auto Merge and Split Edges & Faces while editing."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/merge.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/tool_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# merge-vertices

Goal: weld points exactly where needed and clean duplicate vertices after imports, rips or mirrors.

## Merge menu (Edit Mode, `M`; Mesh > Merge)

- **At Center**: all selected vertices to their geometric center (average position, not bounding box center).
- **At Cursor**: to the 3D cursor (place the cursor first for exact spots).
- **Collapse**: each island of connected vertices becomes one vertex at its average position.
- **At First / At Last**: into the vertex selected first or last; only in Vertex select mode and depends on selection order, which is lost by changing select mode, so run it right after selecting.
- **By Distance**: merges each cluster of vertices closer than *Merge Distance*. Options: *Centroid Merge* (average position instead of the original vertex nearest it), *Unselected* (allow merging selected into unselected vertices), *Sharp Edges* (on smooth-shaded meshes with custom split normals, adds sharp edge marks so sharp edges stay sharp).
- The redo panel for the other types has **Type** and **UVs** (corrects UVs to avoid texture distortion).
- The Weld modifier does merge-by-distance non-destructively.

## Auto Merge (Sidebar > Tool > Options)

- **Auto Merge**: while transforming, a vertex that comes closer to another than *Threshold* merges with it. It affects interactive operations only (redo-panel tweaks count as interactive). Combine with snapping for exact welds.
- **Split Edges & Faces**: detects where a transformed edge intersects others and creates a vertex there, splitting edges and faces.

## Typical cleanups

- Imported meshes with every face separate: Select All, Merge > By Distance, then check shading.
- After applying a Mirror modifier: merge the centre seam if the modifier's merge was off.
- Removing an unwanted edge loop: use Dissolve or Delete > Edge Loops rather than Collapse.

## Gotchas

- Large distances fuse intended detail such as thin walls; raise the value gradually.
- At First/Last: box select loses selection order; click vertices in order.

## Verify

After By Distance, running it again on a clean mesh removes nothing; Select All by Trait > Non Manifold only selects true borders.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Merge and Tool Settings pages: every Merge menu entry, By Distance options, Auto Merge, Threshold and Split Edges & Faces. Removed the unconfirmed 0.0001 default, the 'formerly Remove Doubles' and '4.1+' remarks, and the status-bar report text.
Method: documentation only; no commands were run.
