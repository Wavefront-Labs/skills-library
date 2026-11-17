---
id: creative-arts.fashion-design.clo-3d.exporting-obj-fbx-gltf-and-alembic
name: exporting-obj-fbx-gltf-and-alembic
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-export, clo-obj-export, gltf-export, fbx-export, alembic-export, uv-maps, 3d-garment-export]
level: practitioner
status: draft
description: "Export CLO garments as OBJ, FBX, glTF and Alembic: single vs multiple objects, thickness, unified UVs, textures, avatar inclusion and animation cache for other 3D tools."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.khronos.org/gltf/
  - https://www.alembic.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exporting OBJ, FBX, glTF and Alembic from CLO

**Goal:** garments that open correctly in other 3D tools (Blender, Maya, Unreal, Unity,
web viewers) with textures and the right geometry.

## Formats
| Format | Use |
|---|---|
| OBJ | Static mesh, widely supported; materials in MTL + texture files |
| FBX | Static or animated; avatar with rig; game engines |
| glTF/GLB | Web and AR viewers, e-commerce 3D; PBR materials packed (GLB) |
| Alembic (ABC) | Animated cloth as point cache for VFX (Maya, Houdini, Blender) |

## Export options (File > Export)
- **Selected vs all** objects; include/exclude avatar.
- **Single object vs multiple objects** (per pattern or per garment).
- **Thin vs thick**: thick adds fabric thickness geometry (better for renders); thin is lighter.
- **Unified UV coordinates**: packs all pattern UVs into one 0-1 space (needed for game
  engines and texture painting).
- Texture export (copy textures alongside), scale/unit (cm vs m), axis conversion.
- Weld/merge vertices at seams option for continuous meshes where needed.

## Mesh quality
- Before export, set particle distance (and use remesh/quad options where available) to
  balance detail and polycount; games need low poly + normal maps.

## Animation
- Record the simulation (Animation mode), then export Alembic or FBX with cache; set frame
  range and fps.

## Gotchas
- Textures missing in the target app: export with textures and relative paths.
- Units mismatch: garments 100x too big or small in the engine.
- Exporting without unified UVs makes texture baking hard.

## Verify
- [ ] Model opens in the target app at correct scale.
- [ ] Textures and UVs display correctly.
- [ ] Polycount within the target budget.
