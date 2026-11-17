---
id: creative-arts.animation.blender.tiny-cad
name: tiny-cad
category: creative-arts
field: animation
product: blender
tags: [blender, tiny-cad, tinycad, cad-tools, mesh-editing, bundled-addons, edge-intersect]
level: practitioner
status: gated
description: "Use tinyCAD mesh tools for CAD-like edits: VTX extend and intersect, V2X intersection vertex, XALL, BIX bisector and CCEN circle construction."
sources:
  - https://docs.blender.org/manual/en/4.1/addons/mesh/tinycad.html
  - https://extensions.blender.org/add-ons/tinycad-mesh-tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# tiny-cad

Goal: precise 2D/3D construction geometry in Edit mode (intersections, bisectors, circle centres) without leaving Blender.

## Install

The Blender 4.1 manual documents tinyCAD as a bundled add-on (author zeffii, GPL) whose functions are prepended to the Edit Mode context menu. The extensions.blender.org listing "tinyCAD Mesh tools" shows a minimum of Blender 4.2, so on current releases install it as an extension. The tool behaviour below comes from the 4.1 manual and was not re-checked against the current extension. (gated: unconfirmed, source is paywalled or blocked)

## Tools

| Tool | Select | Result |
|---|---|---|
| **VTX** | two co-planar edges (Edit Mode, edge mode) | automatically picks V (extend both towards their calculated intersection), T (extend one edge towards another) or X (edges cross; the intersection gets a weld vertex); it reports if the edges are not co-planar or do not intersect |
| **V2X** | two edges | places a new separate vertex at the projected intersection |
| **XALL** | a collection of edges | deselects edges that intersect nothing, then repeatedly intersects all combinations until no intersections remain |
| **BIX** | two edges | creates the bisector of the edges (after a co-planarity check) |
| **CCEN** | three vertices | constructs a circle and its centre: adds a Grease Pencil representation of the circle, and F6 afterwards can add a mesh circle (Make Circle Mesh); the manual calls it a little experimental |

## Workflow examples

- Clean intersections in floor plans: draw wall centre lines as edges, select all, *XALL*, then extrude.
- Find an arc's circle from an imported drawing: select three points on the arc and run *CCEN* (practice).

## Gotchas

- VTX needs co-planar edges and reports when it cannot act.
- XALL checks all combinations of edges, so large selections may be slow; work in sections (practice).
- Merge by distance afterwards to remove near-duplicates (practice).

## Verify

After VTX, the two edges share a vertex at the intersection; check its coordinates in the Sidebar.

## Checked

2026-10-27, Blender manual 4.1 (add-on docs) and extensions.blender.org. Confirmed against the Blender 4.1 manual page mesh/tinycad (tool behaviour, location, author, licence) and the extensions.blender.org listing for tinyCAD Mesh tools (minimum Blender 4.2), both fetched on this date. Removed E2F (not in the manual page), the trim wording for VTX, and the cursor claim for CCEN (the manual says it adds a Grease Pencil circle). Current extension behaviour was not re-checked, so it is gated.

Method: documentation only; no commands were run.
