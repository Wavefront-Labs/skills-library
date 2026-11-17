---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-material-sharing-and-program-caching
name: threejs-material-sharing-and-program-caching
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-materials, material-cloning, shader-programs, compileasync, shader-warmup]
level: advanced
status: docs-checked
description: "Share and clone three.js materials without shader stalls: when programs are reused, what forces recompiles, customProgramCacheKey, and precompiling with compileAsync."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/materials/Material.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/webgl/WebGLPrograms.js", "https://github.com/mrdoob/three.js/blob/r186/src/renderers/shaders/UniformsUtils.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/MeshStandardMaterial.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# three.js material sharing and program caching

## 1. Material vs program
A **material** holds parameters (colour, maps, uniforms). A **program** is the compiled shader.
three keys programs on material type plus defines derived from parameters (which maps exist,
fog, skinning, shadows, light counts, tone mapping...). Many materials can share one program.

## 2. Share materials, clone when needed
- Same look on many meshes: assign the **same material instance** (also lets three batch state changes).
- Per-object colour: clone (`mat.clone()` shares textures, copies uniforms) or keep one material
  and use vertex colours / `InstancedMesh.setColorAt` / a uniform per draw via `onBeforeRender`.
- `ShaderMaterial.clone()` deep-copies its uniforms (`cloneUniforms`): vectors, colours and textures held in uniforms
  become new objects, and render-target textures are replaced with `null` (with a warning).

## 3. What triggers recompiles
- Adding/removing a map (null to texture), toggling `transparent`, `alphaTest`, `vertexColors`,
  `flatShading`, `fog`, changing number of lights or shadow-casting lights, changing tone mapping
  or output colour space. Each new combination compiles a new program the first frame it is seen (a hitch).
- Changing a uniform value or a texture to another of the same kind does not recompile.
- `onBeforeCompile` materials: the default `customProgramCacheKey()` returns `onBeforeCompile.toString()`, so patches
  that differ only through closure values need a `customProgramCacheKey()` that returns a distinguishing string.

## 4. Warm up
```js
await renderer.compileAsync(scene, camera);   // uses KHR_parallel_shader_compile where available
renderer.render(scene, camera);
```
Include objects that are hidden now but appear later (temporarily set visible), and every light
configuration you will use. Keep light counts constant; dim lights instead of removing them.

## Gotchas
- `renderer.info.programs.length` climbing during play = recompiles; log `program.name`/cacheKey to find the cause.
- Disposing a material releases its program only when no other material uses it.

## Verify
- [ ] No new programs created after the loading screen (watch renderer.info.programs).
- [ ] First appearance of an effect causes no frame-time spike.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), source of the files in `sources`.
Confirmed: `Material.customProgramCacheKey()` default is `onBeforeCompile.toString()`; `compileAsync` uses
`KHR_parallel_shader_compile`; the program key includes light counts, tone mapping, output colour space, alphaTest,
vertexColors, flatShading, fog and map flags (WebGLPrograms.js); built-in material `copy()` shares texture references
(MeshStandardMaterial.js); `cloneUniforms` deep-copies uniform objects and nulls render-target textures;
`renderer.info.programs` lists compiled programs.

Method: documentation only; no commands were run.
