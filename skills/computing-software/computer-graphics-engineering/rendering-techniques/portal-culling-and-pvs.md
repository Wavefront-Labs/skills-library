---
id: computing-software.computer-graphics-engineering.rendering-techniques.portal-culling-and-pvs
name: portal-culling-and-pvs
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, portal-culling, pvs, potentially-visible-sets, occlusion-culling, indoor-rendering]
level: practitioner
status: draft
description: "Cull indoor scenes with portals and potentially visible sets: cell/portal graphs with frustum narrowing, precomputed PVS baking, and tools like Umbra-style occlusion data."
sources: ["https://www.realtimerendering.com/", "https://docs.unity3d.com/Manual/OcclusionCulling.html", "https://fabiensanglard.net/quakeSource/quakeSourceRendition.php"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Portals and potentially visible sets (PVS)

## 1. Cells and portals
Split indoor levels into **cells** (rooms) connected by **portals** (convex polygons: doors,
windows). Rendering from the camera's cell:
1. Draw the current cell.
2. For each portal of the cell visible in the current frustum, clip the frustum to the portal's
   screen-space bounds (or build planes from the eye through the portal edges) and recurse into the
   neighbouring cell with the narrowed frustum.
3. Stop when the narrowed frustum is empty or depth limit reached; mark visited per path to avoid
   infinite loops through cyclic portals.
Runtime-computed, handles dynamic doors (closed door = disabled portal). Mirrors/teleports are
special portals with a transform.

## 2. Precomputed PVS
For each cell (or view volume), precompute the set of cells/objects that can possibly be visible
from anywhere inside it; store as bitsets.
- Quake: BSP leaves with PVS computed by `vis` tool (portal flow), compressed with RLE.
- Modern: Umbra (used by Unity's built-in occlusion culling) voxelises the scene, generates cells
  and portals automatically, and stores a compact occlusion database queried at runtime.
- Runtime cost: a lookup; build cost: minutes to hours; static geometry only (dynamic objects tested
  against visible cells' bounds).

## 3. Unity occlusion culling
Mark static occluders/occludees, set Smallest Occluder and Smallest Hole, bake (Window > Rendering
> Occlusion Culling). Use Occlusion Areas to limit where the camera can be.

## 4. When to use
- Indoor, corridor-heavy levels: portals/PVS give massive savings cheaply.
- Open worlds: GPU occlusion culling (Hi-Z, two-phase) is more appropriate.

## Gotchas
- PVS is conservative at cell granularity: large cells see too much; fine cells cost memory.
- Portals must be placed at real openings; leaky geometry ruins automatic generation.
- Rebake after level edits; stale PVS hides geometry incorrectly.

## Verify
- [ ] Visualise visible cells from various positions; no popping when walking through doors.
- [ ] Draw counts drop in enclosed areas.
