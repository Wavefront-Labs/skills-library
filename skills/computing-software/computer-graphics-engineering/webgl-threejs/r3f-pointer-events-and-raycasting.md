---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-pointer-events-and-raycasting
name: r3f-pointer-events-and-raycasting
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, r3f-events, pointer-events, raycasting, stoppropagation]
level: practitioner
status: docs-checked
description: "Handle clicks and hovers in React Three Fiber: onClick/onPointerOver on meshes, propagation and stopPropagation, pointer capture, instanced events, and raycast performance."
sources: ["https://r3f.docs.pmnd.rs/api/events", "https://r3f.docs.pmnd.rs/api/canvas#custom-event-manager", "https://github.com/pmndrs/drei#bvh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pointer events and raycasting in R3F

## 1. Events on objects
```jsx
function Box(props) {
  const [hovered, setHovered] = useState(false);
  useCursor(hovered);                               // drei: pointer cursor
  return (
    <mesh {...props}
      onClick={(e) => { e.stopPropagation(); select(e.object); }}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); }}
      onPointerOut={() => setHovered(false)}
      >
      <boxGeometry /><meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>);
}
```
The event carries three's intersection data plus `eventObject` (the object that registered the handler), `camera`, and `delta` (distance in pixels between pointer down and up). `onPointerMissed` fires on clicks that hit no mesh; the R3F docs show it on `<Canvas>`.

## 2. Propagation rules
`e.stopPropagation()` stops the event bubbling up and also stops it being delivered to farther objects (behind this one); objects that had received `pointerover` get `pointerout`. An object that should block events behind it needs a handler that calls `e.stopPropagation()`.

## 3. Drag with capture
```jsx
onPointerDown={(e) => { e.stopPropagation(); e.target.setPointerCapture(e.pointerId); }}
onPointerUp={(e) => e.target.releasePointerCapture(e.pointerId)}
onPointerMove={(e) => dragging && move(e.point)}
```
`setPointerCapture` / `releasePointerCapture` exist only on `event.target` and do not support multiple active pointers. Disable orbit controls during drags.

## 4. Instances and performance
- Large scenes: wrap them in drei `<Bvh firstHitOnly>` (three-mesh-bvh option).
- `<Canvas eventSource={rootEl}>` listens on another DOM element; by default R3F uses offsetX/offsetY and `eventPrefix="client"` changes that.

## Gotchas
- `onClick` fires after a drag too: check `e.delta` to ignore orbit drags.
- A custom event manager (`events.compute`) defines how pointer events become the raycaster and pointer vector.

## Verify
- [ ] Hover highlights only the front-most object.
- [ ] Orbit-dragging does not trigger selection.

## Checked

2026-10-28. Confirmed in the R3F events and Canvas pages: `stopPropagation` semantics, `onPointerMissed`, `eventObject`, `camera`, `delta`, pointer capture only via `event.target` (single pointer), `eventSource`, `eventPrefix="client"`, custom `compute`; drei README: `Bvh` with `firstHitOnly` (three-mesh-bvh), `useCursor`.
Removed (not in the fetched pages): `instanceId`, `face`/`uv`/`ray`/`nativeEvent` field list, `makeDefault` controls, `raycaster` Points threshold and layers, `raycast={() => null}`, the delta threshold of 2, the HTML-overlay claim.

Method: documentation only; no commands were run.
