---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgl-to-webgpu-migration
name: webgl-to-webgpu-migration
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [webgpu, webgl, threejs, wgsl, glsl, compute-shader, browser-graphics, feature-detection, fallback, nodematerial, wgsl-migration, browser-support]
level: advanced
status: draft
description: "Plan a WebGL-to-WebGPU migration (or dual support) in the browser: API model differences, WGSL vs GLSL, compute shader access, browser support reality, and three.js's WebGPURenderer path."
sources: ["https://gpuweb.github.io/gpuweb/", "https://threejs.org/manual/#en/webgpu"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebGL to WebGPU migration

**Goal:** decide whether/how to adopt WebGPU for a browser graphics project —
what it actually buys you, what breaks, and how to ship a fallback rather than
betting the whole project on browser support that isn't universal yet. Status:
draft — WebGPU's browser support and three.js's WebGPU path were both moving
targets as of this writing; re-check current support tables before committing.

## What WebGPU actually adds over WebGL
- **Real compute shaders** in the browser — WebGL 2 has no compute shader
  stage at all; GPGPU work in WebGL means abusing fragment shaders to write to
  a render target (encode data as colors, read back as a "texture"). WebGPU's
  compute pipeline is a first-class citizen, closer to native
  Vulkan/D3D12/Metal compute.
- **Explicit resource/pipeline model** closer to Vulkan/D3D12 (bind groups ≈
  descriptor sets, pipeline layouts, explicit command encoding) rather than
  WebGL's OpenGL-ES-2010s binding model — more verbose setup, more predictable
  performance, less hidden driver-side validation/translation cost per draw.
- **Lower CPU overhead at scale**: command encoding and bind-group reuse avoid
  much of WebGL's per-draw state-validation cost — matters most at high draw-call
  counts, less so for typical low-draw-call web scenes.

## Browser support reality (check before committing)
- WebGPU shipped in Chrome/Edge first, with Firefox and Safari following on
  different timelines and with historically narrower feature coverage
  (compute shader support, specific texture formats) — a project that needs
  universal browser reach still needs a WebGL fallback path, full stop, as of
  this writing. Don't treat WebGPU as a drop-in replacement for public-facing
  web content without checking current browser + OS version matrices.
- Mobile support (especially older Android WebViews, embedded browsers) lags
  further behind desktop — if mobile reach matters, this is often the deciding
  factor to stay on WebGL or dual-support rather than require WebGPU.

## three.js's dual-renderer path
- Modern three.js ships both `WebGLRenderer` and `WebGPURenderer`, with
  `NodeMaterial`-based materials able to compile to either backend from one
  shader graph — this is the practical migration path: author in the node
  system rather than hand-written GLSL, and the same material works on both
  renderers, falling back to WebGL where WebGPU isn't available.
- Hand-written `ShaderMaterial` (raw GLSL) does **not** automatically work on
  `WebGPURenderer` — GLSL and WGSL are different languages; a raw-GLSL
  `ShaderMaterial` is WebGL-only unless rewritten in WGSL or ported to
  `NodeMaterial`. This is the single biggest migration cost for a project with
  significant custom-shader investment.

## WGSL vs GLSL
- WGSL (WebGPU Shading Language) is a new syntax (closer to Rust in style) —
  not a transpile target from GLSL in general; expect to hand-port nontrivial
  custom shaders rather than mechanically translate them. Core concepts
  (vertex/fragment stages, uniforms → bind groups, textures/samplers as
  separate bindings rather than combined sampler types) map over but the
  binding model differs enough that a 1:1 line translation isn't the full job.

## Verify
- [ ] Current browser/OS support matrix checked against the project's actual
      required reach before choosing WebGPU-only.
- [ ] Custom GLSL `ShaderMaterial` usage inventoried — each one is migration
      work (WGSL rewrite or NodeMaterial port), not automatic, if moving to
      `WebGPURenderer`.
- [ ] Feature-detection fallback (`navigator.gpu` check → WebGLRenderer if
      absent) implemented and tested on a browser/device that actually lacks
      WebGPU, not just assumed to degrade gracefully.
- [ ] Compute-shader-dependent features confirmed to have a WebGL-era fallback
      (fragment-shader GPGPU trick) or an explicit "unavailable" UI state for
      WebGPU-less browsers.
