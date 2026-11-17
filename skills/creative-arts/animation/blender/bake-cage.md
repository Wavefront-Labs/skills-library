---
id: creative-arts.animation.blender.bake-cage
name: bake-cage
category: creative-arts
field: animation
product: blender
tags: [blender, bake-cage, cage-extrusion, max-ray-distance, selected-to-active, high-to-low, texture-baking]
level: advanced
status: docs-checked
description: "Bake high-poly detail onto a low poly with Selected to Active: extrusion, max ray distance, custom cage objects, and fixing missed rays, skewed details and seams."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/object/object_bake_api.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# bake-cage

Goal: a clean normal/AO projection from sculpt to game mesh without holes, wavy edges or detail bleeding.

## Selection order

Select the high poly(s), then shift-select the low poly last so it is **active**. Bake panel → *Selected to Active* on. The low poly holds the active Image Texture node and UVs. Rays are cast from the low-poly object inwards towards the high-poly object.

## Extrusion and Max Ray Distance

If the high poly is not entirely enclosed by the low poly, adjust where the rays start:
- *Extrusion* (shown as *Cage Extrusion* when *Cage* is on): distance the active object is inflated for the inward ray cast. Use just enough to enclose the high poly everywhere.
- *Max Ray Distance*: maximum distance for matching points between the active and selected objects; 0 means no limit. Raise it only as far as needed, so rays do not hit unrelated parts.

Too small an extrusion leaves holes where the high poly sticks out; too large lets rays hit the wrong surface.

## Custom cage

1. Duplicate the low poly. The cage needs the same topology (number of faces and face order), so do not change the topology afterwards.
2. Inflate and hand-fix the duplicate until it encloses the high poly.
3. Bake panel → *Selected to Active* → *Cage* on, *Cage Object* = the duplicate. The Cage Extrusion field becomes inactive once a Cage Object is set.
4. A cage whose face count differs from the active object fails with "Invalid cage object, the cage mesh must have the same number of faces as the active object".

## Hard edges

Without a cage, rays follow the mesh normals, which produces glitches on the edges; that is preferable only when baking into planes. Hard splits (for example an applied Edge Split modifier) lead to non-smooth normals around the edges. The inward rays are cast from a version of the active object with Edge Split modifiers disabled, so avoid relying on hard splits for the bake.

## Gotchas

- Glitches along edges: turn *Cage* on or build a custom Cage Object.
- Details from both sides of thin parts: lower Max Ray Distance or bake parts separately.
- Mirrored UV islands that overlap give mixed bakes; offset them during the bake.
- Each object used as a bake source has a fixed CPU memory footprint; join the high-poly objects before baking to avoid out-of-memory crashes.

## Verify

Inspect the baked normal map in the Image Editor: no flat-colour (128,128,255) holes inside detail areas, no doubled features; apply it to the low poly and check silhouette-adjacent areas in Material Preview.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Selected to Active ray direction, Cage, Cage Object, Cage Extrusion, Max Ray Distance and the same-topology requirement (baking page); UI field layout, "0 = no limit" and the "Invalid cage object" message (object_bake_api.cc, ui.py). Removed unsupported numbers (0.01-0.05 m) and the stale "extra offset" claim.

Method: documentation only; no commands were run.
