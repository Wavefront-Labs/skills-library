---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-shadermaterial-and-custom-materials
name: r3f-shadermaterial-and-custom-materials
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, r3f-shadermaterial, drei-shadermaterial, extend, custom-shader-material]
level: practitioner
status: docs-checked
description: "Write custom shaders in React Three Fiber: drei shaderMaterial plus extend, animating uniforms in useFrame, hot-reload keys, CustomShaderMaterial and TypeScript JSX typing."
sources: ["https://drei.docs.pmnd.rs/shaders/shader-material", "https://r3f.docs.pmnd.rs/api/objects#using-3rd-party-objects-declaratively", "https://github.com/FarazzShaikh/THREE-CustomShaderMaterial"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom shader materials in R3F

## 1. drei shaderMaterial + extend
```jsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';
const WaveMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color('hotpink'), uMap: null },
  /* glsl */`varying vec2 vUv; uniform float uTime;
    void main() { vUv = uv; vec3 p = position; p.z += sin(p.x * 4.0 + uTime) * 0.1;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`,
  /* glsl */`varying vec2 vUv; uniform vec3 uColor;
    void main() { gl_FragColor = vec4(uColor * vUv.y, 1.0); }`);
extend({ WaveMaterial });

function Wave() {
  const mat = useRef();
  useFrame((_, dt) => { mat.current.uTime += dt; });     // uniforms exposed as properties
  return <mesh><planeGeometry args={[2, 2, 64, 64]} /><waveMaterial ref={mat} uColor="orange" /></mesh>;
}
```
Uniforms become props (`uColor="orange"` works via three's `set`). Mutate in useFrame, never via React state (re-render per frame).

## 2. Extend built-in materials instead
`three-custom-shader-material` (CSM) keeps PBR lighting, shadows and fog:
```jsx
<CustomShaderMaterial baseMaterial={THREE.MeshStandardMaterial} vertexShader={vs} fragmentShader={fs}
  uniforms={uniforms} color="white" />
```
Write to the `csm_*` outputs (for example `csm_DiffuseColor`, listed in the README). Use it instead of a raw ShaderMaterial when you want the base material's lighting.

## 3. TypeScript
TypeScript needs the JSX namespace extended for anything added with `extend` (R3F docs, using 3rd-party objects). The declaration syntax differs between R3F majors: copy it from the docs of the version you use.

## Gotchas
- Components added with `extend` are referenced in JSX in camelCase (`WaveMaterial` becomes `<waveMaterial />`).

## Verify
- [ ] Animation runs without React re-renders (React DevTools profiler idle).
- [ ] The custom element renders after `extend` and, in TypeScript, the JSX namespace is extended.

## Checked

2026-10-28. Confirmed: `extend` and camelCase JSX naming, and the TypeScript JSX extension requirement (R3F "using 3rd-party objects" page); `baseMaterial` and the `csm_*` output names (three-custom-shader-material README). A preprocessor `#include` was removed from the fragment shader sample because it sat mid-line after `gl_FragColor`.
Removed (not in the fetched pages): `key={WaveMaterial.key}` hot-reload claim, R3F v8/v9 typing snippets, uniform-stability, `depthWrite` and `toneMapped` gotchas, onBeforeCompile comparison.

Method: documentation only; no commands were run.
