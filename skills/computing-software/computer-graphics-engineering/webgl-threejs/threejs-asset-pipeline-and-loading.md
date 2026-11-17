---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-asset-pipeline-and-loading
name: threejs-asset-pipeline-and-loading
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [threejs, webgl, gltf, draco, ktx2, basis-universal, asset-loading, texture-compression, geometry-compression, loadingmanager, dispose, memory-leak, cdn, meshopt]
level: advanced
status: draft
description: "Build a production three.js asset pipeline: glTF as the standard format, Draco/meshopt geometry compression, KTX2/Basis texture compression, loading progress, and the dispose() memory-leak trap."
sources: ["https://threejs.org/docs/#examples/en/loaders/GLTFLoader", "https://github.com/KhronosGroup/glTF", "https://discourse.threejs.org/t/how-to-dispose-of-objects/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three.js asset pipeline and loading

**Goal:** get 3D assets into the browser fast and without leaking GPU memory —
the two problems that aren't obvious until a scene with real asset counts runs
for a while.

## glTF as the standard interchange format
- Use **glTF 2.0** (`.gltf`/`.glb`) as the pipeline's target format, not raw
  OBJ/FBX loaded directly in the browser — glTF is explicitly designed for
  runtime delivery (compact, PBR material model matches three.js's
  `MeshStandardMaterial` directly, supports compression extensions).
- Export from DCC tools (Blender's glTF exporter, etc.) rather than hand-rolling
  — covers skinning, morph targets, animations, and material mapping correctly.
- `GLTFLoader` needs a `DRACOLoader`/`KTX2Loader`/`MeshoptDecoder` instance
  attached (`loader.setDRACOLoader(...)`) if the file uses those compression
  extensions — loading a Draco-compressed glTF without setting the decoder
  fails silently/throws, a common first-integration bug.

## Geometry compression
- **Draco**: quantizes and entropy-codes vertex attributes — large size
  reduction (often 5-10x), at a CPU decode cost on load (WASM decoder) and a
  one-time encode step in the pipeline. Good default for static meshes where
  load-time size matters more than decode CPU cost.
- **meshopt** (`EXT_meshopt_compression`): optimizes vertex/index layout for
  GPU cache efficiency *and* compresses, with typically faster decode than Draco
  — increasingly preferred for web delivery where decode latency matters (e.g.
  streaming many small assets) over Draco's higher compression ratio.
- Don't compress small assets where decoder overhead (loading the WASM decoder
  itself) exceeds the size savings — compression pays off on medium/large meshes,
  not a handful of tiny props.

## Texture compression
- **KTX2 + Basis Universal** (`KTX2Loader`): GPU-compressed texture format,
  transcoded at load time to whatever the device's GPU natively supports
  (ASTC/ETC2/BC7/etc.) — dramatically smaller download AND smaller GPU memory
  footprint than a decoded PNG/JPEG, since it stays compressed in VRAM.
  This is the correct answer to "my scene has 50 textures and uses too much
  GPU memory" — raw PNG/JPEG decode to full RGBA8 in VRAM regardless of the
  compressed download size.
- Without KTX2, a 2K PNG texture uses the same ~16MB of VRAM as if it were
  uncompressed, no matter how small the downloaded file was — download size and
  GPU memory footprint are separate problems, and only GPU-native compressed
  formats solve the second one.

## Loading progress and management
- `THREE.LoadingManager` aggregates progress across multiple loaders/assets for
  a single progress bar — attach it to every loader used (`GLTFLoader`,
  `TextureLoader`, etc.) rather than tracking each asset's promise manually.
- Preload/prioritize critical-path assets (first-visible scene) separately from
  background/lower-priority assets rather than one flat queue, if initial load
  time matters (it almost always does for a web experience).

## The dispose() memory leak
- Removing an object from the scene graph (`scene.remove(mesh)`) does **not**
  free its GPU resources (geometry buffers, textures, compiled shader programs)
  — they remain allocated on the GPU until explicitly disposed:
  `geometry.dispose()`, `material.dispose()`, and for every texture on the
  material, `texture.dispose()`. A scene that swaps assets repeatedly (level
  streaming, configurators) without this leaks GPU memory until the tab crashes
  or the browser evicts the WebGL context.
- Shared resources (a texture/material reused across many meshes) must only be
  disposed once all users are gone — track reference counts or dispose only at
  the point you know nothing else references it, not per-mesh-removal.

## Verify
- [ ] Draco/KTX2/meshopt decoders attached to the loader before loading any
      compressed asset; failure mode (silent hang vs error) checked.
- [ ] GPU memory footprint measured (browser dev tools / `renderer.info.memory`)
      with and without KTX2 texture compression to confirm it's actually engaged.
- [ ] Every removed scene object's geometry/material/textures explicitly
      disposed, verified by watching GPU memory stay flat across repeated
      add/remove cycles.
- [ ] Shared resource disposal checked for premature disposal while still
      referenced elsewhere.
