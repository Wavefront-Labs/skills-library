---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-usegltf-and-suspense-loading
name: r3f-usegltf-and-suspense-loading
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, r3f, usegltf, suspense, useloader, preload, gltfjsx]
level: practitioner
status: docs-checked
description: "Load models in React Three Fiber with useGLTF/useLoader under Suspense: fallbacks, preload, gltfjsx components, Draco/meshopt, and progress UI."
sources: ["https://r3f.docs.pmnd.rs/tutorials/loading-models", "https://github.com/pmndrs/gltfjsx", "https://drei.docs.pmnd.rs/loaders/gltf-use-gltf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useGLTF and Suspense loading

## 1. Load with Suspense
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
function Model(props) {
  const { scene } = useGLTF('/models/chair.glb');     // suspends until loaded, cached by URL
  return <primitive object={scene} {...props} />;
}
function Loader() { const { progress } = useProgress(); return <Html center>{progress.toFixed(0)} %</Html>; }
<Canvas><Suspense fallback={<Loader />}><Model /></Suspense></Canvas>
useGLTF.preload('/models/chair.glb');                  // start fetching at module load
```
`useGLTF` loads Draco binaries from a CDN by default (only for compressed models); pass a path to use your own: `useGLTF(url, '/draco-gltf')` (drei docs). The gltfjsx README also lists meshopt support.

## 2. gltfjsx
```bash
npx gltfjsx chair.glb --transform --types
```
`--types` adds TypeScript definitions. `--transform` produces a compressed copy for the web (draco, prune, resize per the CLI help; the README describes it as using glTF-Transform).

## 3. Reusing a model
For several copies of one model use the drei `Clone` helper or the gltfjsx `Instances` output rather than mounting the same `scene` object twice.

## Verify
- [ ] Network shows assets fetched once; second mount of the model is instant.

## Checked

2026-10-28. Confirmed: `useGLTF.preload`, `Suspense` with a `Loader` fallback (R3F loading-models tutorial); Draco CDN default and own-path option (drei useGLTF page); gltfjsx `--types`, `--transform` (draco, prune, resize), Draco and meshopt support, `Instances` for re-use (gltfjsx README); drei `Clone` exists.
Removed (not in the fetched pages): `SkeletonUtils.clone`, "using `primitive` twice moves it", loader list for textures/KTX2/FBX, the three Gotchas bullets (nested Suspense, error boundary, URL change).

Method: documentation only; no commands were run.
