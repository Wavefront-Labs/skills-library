---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-depth-texture-in-passes
name: threejs-depth-texture-in-passes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-postprocessing, three-depthtexture, depth-buffer, linearize-depth, soft-particles]
level: advanced
status: draft
description: "Attach a DepthTexture to a three.js render target and read it in shaders: linearising depth, reconstructing view position, soft particles, fog and depth-based effects."
sources: ["https://threejs.org/docs/#api/en/textures/DepthTexture", "https://threejs.org/examples/#webgl_depth_texture", "https://threejs.org/docs/#api/en/renderers/shaders/ShaderChunk"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Depth textures in three.js passes

## 1. Render target with depth
```js
const rt = new THREE.WebGLRenderTarget(w, h);
rt.depthTexture = new THREE.DepthTexture(w, h);
rt.depthTexture.type = THREE.UnsignedIntType;     // or FloatType for precision
renderer.setRenderTarget(rt); renderer.render(scene, camera); renderer.setRenderTarget(null);
```
EffectComposer: give its render targets a depthTexture, or render a separate depth pre-pass.

## 2. Read and linearise
```glsl
#include <packing>
uniform sampler2D tDepth; uniform float cameraNear, cameraFar;
float viewZ(vec2 uv) {
  float d = texture2D(tDepth, uv).x;
  return perspectiveDepthToViewZ(d, cameraNear, cameraFar);   // negative, view space
}
float linear01(vec2 uv) { return viewZToOrthographicDepth(viewZ(uv), cameraNear, cameraFar); }
```
Orthographic cameras: depth is already linear (`orthographicDepthToViewZ`).
Logarithmic depth buffer (`logarithmicDepthBuffer: true`) writes `gl_FragDepth` differently: these helpers give wrong values.

## 3. View-position reconstruction
```glsl
vec3 viewPos(vec2 uv) {
  float z = texture2D(tDepth, uv).x * 2.0 - 1.0;
  vec4 clip = vec4(uv * 2.0 - 1.0, z, 1.0);
  vec4 v = cameraProjectionMatrixInverse * clip;  return v.xyz / v.w;
}
```
Basis for SSAO, SSR, decals and world-space fog in post.

## 4. Soft particles / intersections
In the particle material sample scene depth at `gl_FragCoord.xy / resolution` and fade alpha by
`smoothstep(0.0, softness, sceneViewZ - particleViewZ)`. The particle pass must not write to the
depth texture it reads (render scene opaque first, then particles with depthWrite false).

## Gotchas
- Reading a depth texture while it is bound as the current target's depth attachment is a feedback loop error.
- MSAA targets (`samples > 0`) resolve colour; depth texture of multisampled targets needs WebGL2 blit support in your release, so check output.
- Precision: 24-bit depth with a tiny near plane gives stair-stepped far depth.

## Verify
- [ ] Debug pass showing linear depth as greyscale looks smooth from near to far.
- [ ] Particles fade where they meet geometry instead of hard-clipping.
