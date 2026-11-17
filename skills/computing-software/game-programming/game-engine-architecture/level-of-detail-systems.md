---
id: computing-software.game-programming.game-engine-architecture.level-of-detail-systems
name: level-of-detail-systems
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, lod-system, level-of-detail, screen-size, hlod, impostors, lod-transitions, mesh-simplification, game-programming]
level: advanced
status: draft
description: "Build LOD systems: screen-size LOD selection, hysteresis, dithered cross-fades, HLOD and impostors for distance, LOD for animation/ticking/shadows, and budget-driven LOD bias."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/hierarchical-level-of-detail-in-unreal-engine", "https://docs.unity3d.com/Manual/LevelOfDetail.html", "https://github.com/zeux/meshoptimizer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Level of detail systems

**Goal:** spend vertices, draw calls, shading and CPU on what covers pixels; distant content stays
cheap without visible popping.

## Selection by screen size
Compute projected size, not distance (handles FOV changes and resolution):
`screenSize = boundingSphereRadius / (distance * tan(fov / 2))` (fraction of screen height).
Each LOD has a threshold (e.g. LOD0 > 0.5, LOD1 > 0.25, LOD2 > 0.1, then cull/impostor). Apply a global
**LOD bias** from quality settings and a dynamic bias when the GPU is over budget.
- **Hysteresis**: switch down at threshold t, back up only above t * 1.1, so objects at the boundary
  do not flicker.

## Transitions
- **Dithered cross-fade** (screen-door): render both LODs briefly with complementary dither masks
  (Unity `LODGroup` Cross Fade, Unreal "Dithered LOD Transition" material option). Works with
  deferred and opaque; costs two draws during the fade.
- Geomorphing (vertex blending) for terrain.
- Keep silhouette and UV seams consistent across LODs; popping is mostly silhouette and lighting
  (normals) changes.

## Generating LODs
Mesh simplification (quadric error metrics; meshoptimizer `meshopt_simplify`, Simplygon, engine
auto-LOD) with targets like 50%/25%/12%; lock borders and UV seams; then review by an artist for
hero assets. Merge materials at far LODs to cut draws.

## Far distance
- **HLOD**: cluster many static objects into one merged, simplified proxy mesh with baked texture
  for distance (Unreal HLOD / World Partition HLOD layers).
- **Impostors / billboards**: octahedral impostors for trees and props.
- Virtualised geometry (Unreal Nanite) replaces discrete mesh LODs for supported content but not
  for everything (check skinned/translucent support per engine version).

## LOD beyond meshes
Animation (lower update rate, fewer bones: Unreal URO, Unity Animator culling mode), ticking (AI and
gameplay update frequency by significance), shadows (no shadow casting at far LODs, cheaper cascades),
materials (simpler shaders), physics (simpler colliders), audio voice priority.

## Verify
- [ ] LOD visualisation mode (colour per LOD) shows expected distribution in a busy scene.
- [ ] No visible popping in a slow camera dolly at typical play distances.
- [ ] Triangle count and draw count drop as expected when the dynamic LOD bias rises.
