---
id: computing-software.computer-graphics-engineering.webgl-threejs.gltf-transform-asset-optimisation
name: gltf-transform-asset-optimisation
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-loading, gltf-transform, meshopt, draco, ktx2, asset-optimisation]
level: practitioner
status: docs-checked
description: "Shrink and speed up glTF assets for the web with the glTF-Transform CLI: inspect, optimize, dedup, prune, weld, simplify and texture compression commands."
sources: ["https://gltf-transform.dev/cli", "https://gltf-transform.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimising glTF with glTF-Transform

## 1. One-shot CLI
```bash
gltf-transform optimize input.glb output.glb --compress draco --texture-compress webp
gltf-transform inspect input.glb
```
The `inspect` report should identify performance issues (geometry-heavy, texture-heavy, too many draw calls). The `optimize` defaults may not suit every scene; see `optimize -h` for its options, or pick individual commands.

## 2. Step by step when you need control
```bash
gltf-transform dedup in.glb a.glb      # deduplicate accessors and textures
gltf-transform prune a.glb a.glb       # remove unreferenced properties
gltf-transform weld a.glb a.glb        # merge equivalent vertices
gltf-transform simplify a.glb a.glb    # reduce vertex count
gltf-transform uastc a.glb a.glb       # KTX + Basis UASTC texture compression
gltf-transform etc1s a.glb a.glb       # KTX + Basis ETC1S texture compression
```
Other commands: `flatten`, `join` (merge meshes, fewer draw calls), `palette`, `resample`, `sparse`, `webp`, `avif`. Run each with `-h` for its flags.

## 3. Loading
The viewer or three.js loader needs a matching decoder for each compression extension used; check the three.js GLTFLoader documentation.

## Gotchas
- Simplify can break UV seams and skinned meshes; check visually per asset.

## Verify
- [ ] `inspect` before/after: file size and VRAM estimate; visual diff in the viewer.

## Checked
2026-11-01. Confirmed against the glTF-Transform CLI page: optimize example, inspect, and the command list (dedup, prune, flatten, join, weld, simplify, palette, etc1s, uastc, webp, avif, resample, sparse). Removed: flag values (--ratio, --error, --slots, --texture-size), toktx requirement, meshopt/Draco/KTX2 comparisons, loader code, ETC1S normal-map advice.
Method: documentation only; no commands were run.
