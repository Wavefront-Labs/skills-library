---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-xr-react-three-xr
name: r3f-xr-react-three-xr
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, react-three-xr, webxr, xr-store, hand-tracking]
level: practitioner
status: docs-checked
description: "Build VR and AR scenes in React Three Fiber with @react-three/xr v6: createXRStore, enterAR, pointer events in XR, origin and teleport."
sources: ["https://pmndrs.github.io/xr/docs/getting-started/introduction", "https://github.com/pmndrs/xr", "https://pmndrs.github.io/xr/docs/tutorials/teleport"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XR in R3F with @react-three/xr

## 1. Setup (v6 API)
```jsx
import { createXRStore, XR, XROrigin, TeleportTarget } from '@react-three/xr';
const store = createXRStore({ hand: { teleportPointer: true }, controller: { teleportPointer: true } });

export default function App() {
  const [pos, setPos] = useState(new THREE.Vector3());
  return (<>
    <button onClick={() => store.enterAR()}>Enter AR</button>
    <Canvas>
      <XR store={store}>
        <XROrigin position={pos} />
        <TeleportTarget onTeleport={setPos}><mesh rotation-x={-Math.PI / 2}><planeGeometry args={[20, 20]} /></mesh></TeleportTarget>
        <Scene />
      </XR>
    </Canvas>
  </>);
}
```
The package README lists a migration guide from @react-three/xr v5; do not mix v5 examples with the store API above.

## 2. Interaction
The README example uses a normal R3F `onClick` on a mesh, triggered by touching or pointing, and `pointerEventsType={{ deny: 'grab' }}` to filter input types. The docs have tutorials for Interactions, Handles, Gamepad, Origin, Teleport, Anchors, DOM overlays and Hit Test.

## 3. Reading XR state
Read the Store, Gamepad, Anchors, Hit Test and DOM Overlay tutorials of the @react-three/xr docs for the hooks and components of the version you install; this skill does not reproduce their names from memory.

## 4. Performance in XR
Check the Store tutorial for the performance options (foveation, frame rate, framebuffer scaling) of your version.

## Gotchas
- `XROrigin` takes a `position`; the teleport tutorial moves it from `TeleportTarget`'s `onTeleport` handler instead of moving the camera.

## Verify
- [ ] Enter VR on device; controller rays click the same UI as the mouse.
- [ ] Teleport moves the origin and keeps floor height correct.

## Checked

2026-10-28. Confirmed in the @react-three/xr README and teleport tutorial: `createXRStore`, `store.enterAR()`, `<XR store>`, `hand` and `controller` `teleportPointer` options, `<XROrigin position>`, `<TeleportTarget onTeleport>`, `pointerEventsType`, the v5 migration guide and tutorial topic list.
Removed (not in the fetched pages): `enterVR`, `foveation`, `frameRate`, `emulate`, `rayPointer` options, `useXR`, `useXRInputSourceState`, `useXRHitTest`, `useXRAnchor`, `XRDomOverlay`, `frameBufferScaling`, `metaQuest3`, v5 API names, emulator and framebuffer claims.

Method: documentation only; no commands were run.
