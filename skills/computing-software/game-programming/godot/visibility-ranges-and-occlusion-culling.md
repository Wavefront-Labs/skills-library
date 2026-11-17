---
id: computing-software.game-programming.godot.visibility-ranges-and-occlusion-culling
name: visibility-ranges-and-occlusion-culling
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-performance, visibility-range, occlusion-culling-godot, hlod-godot, game-programming]
level: practitioner
status: docs-checked
description: "Cut Godot 3D rendering cost with visibility ranges (manual LOD/HLOD with fade), automatic mesh LOD, OccluderInstance3D baking and VisibleOnScreenNotifier3D logic culling."
sources: ["https://docs.godotengine.org/en/stable/tutorials/3d/visibility_ranges.html", "https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visibility ranges and occlusion culling

**Goal:** large 3D scenes render only what matters at each distance.

## Visibility ranges (GeometryInstance3D)
- `visibility_range_begin` / `visibility_range_end` (+ begin and end margins): the node is visible only
  between those distances, measured from the camera to the centre of the instance's AABB. Works with any
  GeometryInstance3D (meshes, MultiMesh, particles, Label3D, Sprite3D, CSG).
- `visibility_range_fade_mode`: Disabled (hysteresis switch, best performance), Self (alpha-blends this
  node, forcing transparent rendering during the fade), Dependencies (fades in dependencies for
  `visibility_parent` HLOD; acts like Self otherwise). Fade mode only matters when a margin is above 0.
- **HLOD**: give the detailed child nodes a `visibility_parent` that points at the low-detail merged
  mesh (a GeometryInstance3D, never one of their own children) and give the merged mesh a begin distance
  above 0; when the camera is far, the merged mesh shows and the children hide.
Example from the docs: a sphere mesh with end 10.0 and end margin 1.0, a box mesh with begin 10.0 and
begin margin 1.0.

## Automatic mesh LOD
Mesh LOD is generated on import for imported 3D scenes (glTF, .blend, Collada, FBX) but not for OBJ meshes
unless imported As Scene; it can be disabled per scene or per mesh in the Import dock or Advanced Import
Settings. Tune `GeometryInstance3D.lod_bias` per instance, `Viewport.mesh_lod_threshold` at runtime, or
Rendering > Mesh LOD > LOD Change > Threshold Pixels (default 1; higher is faster but lower quality).
Mesh LOD and visibility ranges can be used together, even on one mesh.

## Occlusion culling
1. Project Settings > Rendering > Occlusion Culling > **Use Occlusion Culling** on.
2. Add `OccluderInstance3D`, click Bake Occluders (bakes the level's geometry; use Bake > Cull Mask and
   visual layers to keep dynamic objects out) or assign a QuadOccluder3D, BoxOccluder3D, SphereOccluder3D
   or PolygonOccluder3D.
3. Most effective in indoor scenes; add opaque walls to break the line of sight.
Debug: Perspective menu > Display Advanced > Occlusion Culling Buffer.

## Logic culling
`VisibleOnScreenEnabler3D` enables its target node (through `process_mode`) only while its box region is on
screen, for example to activate enemies when the player approaches; `VisibleOnScreenNotifier3D` only
reports visibility through signals.

## Measuring
In the 3D viewport's Perspective menu enable View Information (primitives drawn) and View Frame Time; the
Disable Mesh LOD and Occlusion Culling Buffer debug draw modes help compare.

## Gotchas
- Dynamic objects can be occludees but should be excluded from baking (Bake > Cull Mask). Avoid moving
  OccluderInstance3D nodes, or their parents, during gameplay.
- Self and Dependencies fade modes force transparent rendering during the fade; Disabled is cheapest.

## Verify
- [ ] Primitives in View Information drop when walking behind large buildings.
- [ ] No pop-in visible at configured fade margins.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: visibility range Begin, End and margins measured to the centre of the instance's AABB; the three fade modes and their transparent-rendering cost; `visibility_parent` HLOD rules (target must be a GeometryInstance3D, not a child); the docs' 10.0 and 1.0 example; mesh LOD generation for imported scenes but not OBJ, `lod_bias` (default 1.0), `mesh_lod_threshold` and Rendering > Mesh LOD > LOD Change > Threshold Pixels (default 1); Use Occlusion Culling project setting, OccluderInstance3D baking with Bake > Cull Mask, the four primitive occluder types, the Occlusion Culling Buffer debug mode, most effective indoors, avoid moving occluders; `VisibleOnScreenEnabler3D` toggles its target's process mode while the Notifier only signals. Removed the unconfirmed monitor-path, split-screen and early-version claims.

Method: documentation only; no commands were run.
