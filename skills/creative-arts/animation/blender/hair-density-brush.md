---
id: creative-arts.animation.blender.hair-density-brush
name: hair-density-brush
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-density-brush, density-brush, add-hair-brush]
level: practitioner
status: docs-checked
description: "Add and thin Blender Curves hair with the Add, Density and Delete brushes: count, interpolation toggles, density mode, minimum distance and count max."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/add_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/density_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/brushes/delete_curves.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hair-density-brush

Curves Sculpt mode brushes that add, remove and thin hair. Most need the Curves object to have a **Surface** set (Curves Data > Surface, UV Map).

## Add brush
Distributes new curves on the surface; they follow surface normals. Settings: **Count**; **Interpolate** toggles Length, Radius, Shape, Point Count (new curves take the average of nearby curves, so new hair is already combed); **Curve Length**, **Curve Radius** and **Points per Curve** are used when not interpolating (Radius interpolation is skipped when there is no radius attribute).

## Density brush
Creates or removes curves based on a target distance: it samples many points and rejects those too close to existing ones. Settings: **Density Mode** (Auto adds or removes depending on root spacing under the cursor; Add; Remove), **Distance Min** (goal distance between roots; Edit Minimum Distance with R sets it interactively), **Count Max** (maximum points sampled on the surface).

## Delete brush
Removes whole curves if any segment falls under the brush radius.

## Practice
Groom a modest number of guides, then raise final density with Interpolate Hair Curves (see hair-interpolate) instead of painting every hair.

## Gotchas
- Brushes do nothing useful without a surface and UV map.
- Curves Sculpt tools only use the original surface mesh, not its modifiers.

## Verify
Paint with Density Mode Auto and a set Distance Min: spacing between roots evens out.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed Add (Count, Interpolate Length/Radius/Shape/Point Count, Curve Length/Radius, Points per Curve), Density (Density Mode, Distance Min, R shortcut, Count Max) and Delete brush behaviour. Removed the Auto-by-default claim, the world-units note, example distances and curve count formula; replaced the generic sources link with the brush pages.
Method: documentation only; no commands were run.
