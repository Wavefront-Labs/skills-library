---
id: computing-software.computer-graphics-engineering.rendering-techniques.gaussian-splat-viewers-and-web-rendering
name: gaussian-splat-viewers-and-web-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, image-based-rendering, splat-rendering, gaussian-splatting, 3dgs, depth-sorting, webgl, webgpu]
level: advanced
status: docs-checked
description: "Render 3D Gaussian splats on the web: PLY, splat, ksplat and SPZ formats, sort strategies, GaussianSplats3D limits and known issues."
sources: ["https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/", "https://github.com/mkkellogg/GaussianSplats3D", "https://github.com/nianticlabs/spz"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gaussian splat viewers and web rendering

## 1. Method and formats
3D Gaussian Splatting (Inria) represents a scene with anisotropic 3D Gaussians and reports real-time
(at least 100 fps) novel-view synthesis at 1080p for unbounded, complete scenes.

| Format | Notes |
|---|---|
| `.ply` | the files produced by the Inria training code |
| `.splat` | standard compact splat file loaded by web viewers |
| `.ksplat` | GaussianSplats3D's own trimmed-down, compressed format matching its internal data layout, giving the fastest load; the author notes it still needs work around compression |
| `.spz` (Niantic) | compressed Gaussian splat format, typically around 10x smaller than the equivalent `.ply` with minimal visual difference; C++ library with a WASM/TypeScript build; stores RUB axes by default, with named coordinate systems selectable in PackOptions and UnpackOptions |

Coordinate conventions differ: SPZ default RUB (OpenGL and three.js), PLY typically RDF, GLB
typically LUF, Unity typically RUF. Specify source and target systems when packing and unpacking
or interoperability can suffer; converting between families also rotates spherical-harmonics
coefficients.

## 2. Web viewer: GaussianSplats3D (three.js)
- Imports `.ply`, `.splat` and `.ksplat`; can convert `.ply` or `.splat` to `.ksplat`.
- Renders a three.js scene or object group along with the splats; built-in WebXR support.
- Spherical harmonics: degree 1 and 2 supported for view-dependent colour.
- Optimisations: splats culled before sorting and rendering with a custom octree; WASM SIMD sort in
  C++; partially GPU-accelerated sort using transform feedback to precompute distances.
- Splat count limits depend on SH degree: about 16 million at degree 0, 11 million at degree 1, 8
  million at degree 2.
- Prior web viewers it built on: antimatter15/splat (WebGL) and cvlab-epfl/gaussian-splatting-web
  (WebGPU).

## 3. Tips and known issues (from the README)
- Progressively loaded `.ply` and `.splat` files miss optimisations such as cache-optimised splat
  ordering; convert to `.ksplat` or load non-progressively for best performance.
- For scenes with large dimensions or high density, set the viewer parameter `integerBasedSort` to
  false (slower floating-point sort) or raise `splatSortDistanceMapPrecision` (reduces artefacts at a
  performance cost).
- The sort runs on the CPU, so artefacts show when moving or rotating too fast.
- Performance on mobile is sub-optimal; very large scenes can crash with an `Index out of bounds`
  error from the sort.

## Verify
- [ ] Reference scene matches the training viewer visually; frame time at target resolution.
- [ ] No sorting artefacts during fast rotation; splat count within the SH-degree limit.
- [ ] Coordinate system specified when converting formats.

## Checked
Method: docs-checked 2026-11-09 against the Inria 3DGS project page (abstract), the GaussianSplats3D README (features, tips, known issues, limits table) and the Niantic spz README (first 80 lines: format size, coordinate systems, build). Removed unconfirmed projection maths, 3-sigma quad, tile and WebGPU engine claims.
