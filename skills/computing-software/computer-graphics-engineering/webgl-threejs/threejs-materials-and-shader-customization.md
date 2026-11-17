---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-materials-and-shader-customization
name: threejs-materials-and-shader-customization
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [threejs, webgl, materials, shadermaterial, onbeforecompile, custom-shaders, pbr, colorspace, tonemapping, outputcolorspace, texture-encoding, uniforms, glsl-chunks]
level: advanced
status: docs-checked
description: "Customize three.js materials correctly: onBeforeCompile vs ShaderMaterial vs NodeMaterial, color-space/tone-mapping pitfalls, and wiring custom uniforms into the built-in PBR shader chunks."
sources: ["https://github.com/mrdoob/three.js/blob/r186/src/renderers/WebGLRenderer.js", "https://github.com/mrdoob/three.js/blob/r186/src/materials/RawShaderMaterial.js", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/color-management.html", "https://github.com/mrdoob/three.js/blob/r186/manual/pages/webgpurenderer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Three.js materials and shader customization

**Goal:** extend or replace three.js materials without breaking color
management or losing the built-in PBR lighting you'd otherwise have to
reimplement from scratch.

## Three ways to customize, in order of how much you keep
- **`onBeforeCompile`**: patch the generated GLSL of a built-in material
  (`MeshStandardMaterial`, etc.) by string-replacing chunks before compilation —
  keeps the full PBR lighting pipeline (IBL, shadows, all light types) and you
  only add/modify specific pieces (e.g. a custom vertex displacement, an extra
  uniform-driven effect). The pragmatic default for "mostly standard PBR plus one
  custom thing."
- **`ShaderMaterial`/`RawShaderMaterial`**: full custom vertex+fragment shaders,
  no built-in lighting — you must implement everything (lighting, shadows, fog)
  yourself if needed. Right choice for genuinely non-standard shading (toon,
  stylised, fully custom VFX) where fighting the PBR pipeline would cost more
  than writing from scratch. `RawShaderMaterial` skips three.js's injected
  uniforms/attributes entirely (even more manual).
- **`NodeMaterial`** (three.js's node-based shader system, newer): compose
  shaders from a graph of nodes, used with WebGPURenderer (WGSL, or GLSL on its
  WebGL 2 backend) — the forward-looking option, at the cost of a
  different (less familiar to raw-GLSL people) authoring model. `ShaderMaterial`,
  `RawShaderMaterial` and `onBeforeCompile` are not supported by WebGPURenderer.

## Color management pitfalls
- three.js defaults `THREE.ColorManagement.enabled = true` and
  `renderer.outputColorSpace = THREE.SRGBColorSpace` — textures loaded as color
  data need `texture.colorSpace = THREE.SRGBColorSpace` set explicitly (or the
  loader's default, which varies by texture type) so they're correctly decoded
  before lighting; **data textures** (normal maps, roughness/metalness, ORM
  packed maps) must stay `THREE.NoColorSpace`/linear — setting sRGB on a normal
  map corrupts it.
- Wrong texture colour spaces show up as colours that look washed out, too dark or too
  saturated; check the colour-management manual page for the release in use.
- `renderer.toneMapping` (ACESFilmic, etc.) + `toneMappingExposure` apply after
  lighting, before output color-space encoding — a custom shader material that
  outputs directly to `gl_FragColor` bypasses three.js's tone-mapping/color-space
  pass unless you explicitly include it (`#include <tonemapping_fragment>` /
  `#include <colorspace_fragment>` chunks, or manual equivalent code) — a
  ShaderMaterial that looks "flat" compared to built-in materials is usually
  missing this.

## Wiring custom uniforms via onBeforeCompile
```js
material.onBeforeCompile = (shader) => {
  shader.uniforms.uTime = { value: 0 };
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    '#include <begin_vertex>\ntransformed.y += sin(uTime + position.x) * 0.1;'
  );
  material.userData.shader = shader;   // keep a reference to update uniforms per frame
};
// per frame:
if (material.userData.shader) material.userData.shader.uniforms.uTime.value = clock.getElapsedTime();
```
- `onBeforeCompile(shader, renderer)` runs when a program variant is first built for the
  material, not every frame. Uniforms added this way live on the captured
  `shader.uniforms`, not on `material.uniforms`, so keep the reference as above.
- Changing `material.defines` or anything that affects the generated shader
  source requires `material.needsUpdate = true` to force recompilation.

## Verify
- [ ] Texture colorSpace set explicitly per texture type (sRGB for albedo/
      emissive, linear for normal/roughness/metalness/AO), not left to loader
      defaults assumed correct.
- [ ] Custom ShaderMaterial output checked against a built-in material's
      brightness/contrast on the same scene — missing tone-mapping/color-space
      chunks shows as a visible mismatch.
- [ ] onBeforeCompile uniform updates verified to actually reach the GPU (via the
      captured `shader` reference), not silently no-op.
- [ ] Three.js version's color-management defaults checked against the version
      actually installed, not assumed from general docs.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), WebGLRenderer.js, RawShaderMaterial.js and the manual pages
on colour management and WebGPURenderer.
Confirmed: `ColorManagement.enabled` is on by default; non-colour textures such as `normalMap` and `roughnessMap` use
`NoColorSpace`; `RawShaderMaterial` does not get built-in uniform and attribute definitions prepended; `onBeforeCompile`
is invoked when a program is built for a cache key and receives the shader parameters object, so uniforms must be
attached to that object; `ShaderMaterial`, `RawShaderMaterial` and `onBeforeCompile` are unsupported in WebGPURenderer;
the `tonemapping_fragment` and `colorspace_fragment` shader chunks exist.

Method: documentation only; no commands were run.
