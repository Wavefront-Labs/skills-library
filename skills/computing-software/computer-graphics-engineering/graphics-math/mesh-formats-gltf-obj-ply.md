---
id: computing-software.computer-graphics-engineering.graphics-math.mesh-formats-gltf-obj-ply
name: mesh-formats-gltf-obj-ply
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, geometry-processing, mesh-formats, gltf, obj, ply, format-conversion]
level: practitioner
status: draft
description: "Choose and convert mesh formats: glTF 2.0 vs OBJ, PLY, STL, FBX, USD; coordinate systems and units, index/attribute layouts, and conversion tools that keep materials intact."
sources: ["https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html", "https://paulbourke.net/dataformats/ply/", "https://trimesh.org/", "https://github.com/KhronosGroup/glTF-Validator"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mesh data formats and conversion

| Format | Contents | Notes |
|---|---|---|
| glTF 2.0 (.gltf/.glb) | Meshes, PBR materials, scene graph, skins, animation | Runtime delivery standard; Y-up, metres, right-handed, CCW front faces |
| OBJ + MTL | Positions, UVs, normals, polygons, simple materials | Separate index per attribute (needs re-indexing for GPUs); no units/axis metadata; 1-based indices |
| PLY | Vertices/faces with arbitrary properties, ASCII or binary | Scans, point clouds, per-vertex colour |
| STL | Triangles only, facet normals | 3D printing; no shared vertices (weld on load), units implied (usually mm) |
| FBX | Full scenes, animation | Proprietary SDK; axis/unit settings per file |
| USD (.usd/.usdz) | Composable scenes | Film/AR pipelines, USDZ for Apple AR |

## Coordinate systems and units
Blender Z-up, glTF/Maya Y-up, Unreal Z-up left-handed in centimetres, Unity Y-up left-handed in
metres. Converting handedness = flip one axis **and** reverse triangle winding. Record units: an STL in
millimetres imported as metres is 1000x too big.

## Conversion
```python
import trimesh
scene = trimesh.load("model.obj")             # keeps MTL materials as PBR approximations
scene.export("model.glb")
```
- Blender CLI: `blender -b -P convert.py` with `bpy.ops.import_scene.fbx` / `bpy.ops.export_scene.gltf(filepath=..., export_format='GLB')`.
- `assimp export in.fbx out.gltf2` for broad format support.
- `gltf-transform` (Node) to optimise glTF: `gltf-transform optimize in.glb out.glb --compress draco --texture-compress webp`.
- Validate glTF with the Khronos glTF-Validator.

## Pitfalls
- OBJ normals/UV seams: re-indexing creates more vertices than positions; that is expected.
- Quads/n-gons must be triangulated for GPUs; triangulation choice affects shading of non-planar quads.
- Vertex colours in PLY may be uint8 or float; sRGB vs linear is undefined, document it.
- Materials rarely survive round trips exactly (Phong MTL to PBR glTF is approximate).

## Verify
Re-import the converted file and compare vertex/triangle counts, bounding box (units, axis), and a
render against the source.
