---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-canvas-and-useframe
name: r3f-canvas-and-useframe
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, r3f, useframe, react-three-fiber, canvas, render-loop]
level: practitioner
status: draft
description: "Set up a React Three Fiber Canvas (camera, gl, dpr, shadows) and animate with useFrame correctly: delta time, refs not state, and priority ordering."
sources: ["https://r3f.docs.pmnd.rs/api/canvas", "https://r3f.docs.pmnd.rs/api/hooks#useframe", "https://r3f.docs.pmnd.rs/advanced/pitfalls"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# R3F Canvas and useFrame

## 1. Canvas
```jsx
import { Canvas } from '@react-three/fiber';
<Canvas camera={{ position: [3, 2, 5], fov: 50, near: 0.1, far: 100 }}
        dpr={[1, 2]} shadows gl={{ antialias: true }} flat={false} linear={false}>
  <ambientLight intensity={0.3} />
  <directionalLight position={[5, 5, 5]} castShadow />
  <Spinner />
</Canvas>
```
The Canvas fills its parent: give the parent a height. Tone mapping (ACES) and sRGB output are
on by default; `flat` disables tone mapping, `linear` disables sRGB conversion.

## 2. useFrame
```jsx
function Spinner() {
  const ref = useRef();
  useFrame((state, delta) => { ref.current.rotation.y += delta; });   // delta in seconds
  return <mesh ref={ref}><boxGeometry /><meshStandardMaterial /></mesh>;
}
```
- Mutate through refs; never `setState` in useFrame (re-renders React 60 times a second).
- Multiply by `delta` so speed is frame-rate independent (120 Hz displays exist).
- `state` gives `camera`, `scene`, `gl`, `clock`, `pointer`, `size`.
- Must be called inside a component under `<Canvas>`; hooks outside throw.

## 3. Priority
`useFrame(cb, 1)` with a non-zero priority **takes over rendering**: you must call
`state.gl.render(state.scene, state.camera)` yourself. Use it for custom render passes; negative
priorities run earlier without taking over.

## Gotchas
- Creating `new THREE.Vector3()` inside useFrame allocates every frame; hoist it.
- Declarative props (`position={[x,y,z]}`) on every render reset what useFrame mutated.
- Event handlers (`onClick`) on meshes use R3F's raycaster; heavy scenes need `raycast` disabled
  on non-interactive meshes.

## Verify
- [ ] React DevTools profiler shows no re-renders while the scene animates.
