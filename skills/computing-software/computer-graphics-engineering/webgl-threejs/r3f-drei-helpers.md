---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-drei-helpers
name: r3f-drei-helpers
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, r3f, drei, orbitcontrols, environment, html-overlay]
level: practitioner
status: draft
description: "Use @react-three/drei helpers well (OrbitControls, Environment, useGLTF, Html, Text, Bounds, ContactShadows, Instances) and know their costs."
sources: ["https://drei.docs.pmnd.rs/", "https://github.com/pmndrs/drei"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# drei helpers

## 1. The usual set
```jsx
import { OrbitControls, Environment, ContactShadows, Html, Text, Bounds, Center, useGLTF } from '@react-three/drei';
<Canvas>
  <Environment preset="city" />                       {/* HDRI from CDN; use files= for self-hosting */}
  <Bounds fit clip observe margin={1.2}><Center><Model /></Center></Bounds>
  <ContactShadows position={[0, -0.5, 0]} opacity={0.5} blur={2} far={1} frames={1} />
  <Html position={[0, 1, 0]} center occlude>Label</Html>
  <Text fontSize={0.2} anchorX="center">Hello</Text>   {/* troika SDF text */}
  <OrbitControls makeDefault />
</Canvas>
```
`makeDefault` lets other helpers (Bounds, CameraControls) find the controls.

## 2. Cost notes
| Helper | Cost |
|---|---|
| `Environment preset` | Fetches HDR from a CDN at runtime; self-host for production (`files="/env.hdr"`) |
| `ContactShadows` | Re-renders the scene from below each frame; `frames={1}` for static scenes |
| `Html` | DOM element per instance; hundreds tank performance; `occlude` raycasts per frame |
| `Text` | SDF generation in a worker on first use; preload fonts |
| `MeshReflectorMaterial`, `MeshTransmissionMaterial` | Extra scene renders per frame |
| `Instances`/`Merged` | Cheap; use for repeated meshes |

## 3. Performance helpers
`<AdaptiveDpr pixelated />`, `<PerformanceMonitor onDecline={...}>`, `<Preload all />`,
`<BakeShadows />`, `<Stats />`.

## Gotchas
- Environment presets fail offline or behind strict CSP.
- Importing everything from drei pulls large deps; tree shaking works with ESM bundlers but check
  bundle size.
- drei versions are tied to R3F majors (drei 10 for R3F 9 / React 19).

## Verify
- [ ] Network tab: no runtime CDN fetches in production; frame time stable.
