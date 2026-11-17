---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-performance-and-frameloop-demand
name: r3f-performance-and-frameloop-demand
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, r3f, r3f-performance, frameloop-demand, invalidate, instancing, regress]
level: advanced
status: docs-checked
description: "Make React Three Fiber apps fast: frameloop demand with invalidate, avoiding re-renders, reusing geometry, instancing, adaptive DPR and performance regression."
sources: ["https://r3f.docs.pmnd.rs/advanced/scaling-performance", "https://r3f.docs.pmnd.rs/advanced/pitfalls", "https://r3f.docs.pmnd.rs/api/canvas#render-props"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R3F performance

## 1. Render on demand
```jsx
<Canvas frameloop="demand">...</Canvas>
const invalidate = useThree(s => s.invalidate);
onChange={() => invalidate()}
```
Only renders when React detects prop changes or `invalidate()` is called. Mutating props outside React (for example orbit controls moving the camera) is invisible to React, so wire `invalidate` to the controls' `change` event. `invalidate()` only requests a frame; many calls before the next frame render once.
Suited to configurators and viewers that are idle most of the time.

## 2. Avoid React work
- Animate via refs in `useFrame`, not state.
- Zustand selectors (`useStore(s => s.x)`) or transient subscriptions instead of context that
  re-renders the tree.
- Do not mount/unmount meshes to hide them: toggle `visible` (the R3F pitfalls page warns that mounting creates and compiles materials and lights).

## 3. Reuse and instance
- Share geometry and materials: define once with `useMemo` or at module scope; JSX
  `<boxGeometry />` per mesh creates a buffer each.
- Many identical objects: `<instancedMesh args={[geo, mat, count]}>`; update with `setMatrixAt` and set `instanceMatrix.needsUpdate = true`.

## 4. Adaptive quality
```jsx
<Canvas dpr={[1, 2]} performance={{ min: 0.5 }}>
  <PerformanceMonitor onDecline={() => setDpr(1)} onIncline={() => setDpr(2)} />
```
`state.performance.regress()` temporarily lowers `performance.current` (toward `min`) during interaction, for example from a controls `change` event. On its own it changes nothing: your app must read `performance.current` (for example scale the pixel ratio by it).

## 5. Measure
Browser profiler for React commits, and `gl.info.render.calls` (three.js `WebGLRenderer.info`).

## Gotchas
- `frameloop="demand"` plus a `useFrame` animation needs `invalidate()` in the loop, or it stops.

## Verify
- [ ] In demand mode the scene stops rendering when nothing changes; controls still trigger frames.

## Checked
2026-11-01. Confirmed against the R3F docs source (`docs/advanced/scaling-performance.mdx`, `docs/advanced/pitfalls.mdx`, `docs/API/canvas.mdx`, `docs/API/hooks.mdx`): `frameloop` demand, `invalidate` semantics and the controls `change` example, `performance={{ min }}` with `regress()` and its opt-in behaviour, `PerformanceMonitor` `onIncline`/`onDecline`, `useMemo` for shared geometry, `visible` toggling, instancedMesh example. `WebGLRenderer.info.render.calls` confirmed in the three.js docs. Removed unconfirmed claims: drei controls calling invalidate, `useGLTF` caching and `<Clone>`, `AdaptiveDpr`, `r3f-perf`, Suspense and strict-mode remarks.
Method: documentation only; no commands were run.
