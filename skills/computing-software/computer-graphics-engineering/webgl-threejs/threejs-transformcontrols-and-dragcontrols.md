---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-transformcontrols-and-dragcontrols
name: threejs-transformcontrols-and-dragcontrols
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-picking, transformcontrols, dragcontrols, gizmo, editor-interaction]
level: practitioner
status: docs-checked
description: "Add editor-style move/rotate/scale gizmos with TransformControls and drag interaction with DragControls in three.js, coordinating with OrbitControls."
sources: ["https://github.com/mrdoob/three.js/blob/r186/examples/jsm/controls/TransformControls.js", "https://github.com/mrdoob/three.js/blob/r186/examples/jsm/controls/DragControls.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TransformControls and DragControls

## 1. TransformControls gizmo
```js
import { TransformControls } from 'three/addons/controls/TransformControls.js';
const tc = new TransformControls(camera, renderer.domElement);
scene.add(tc.getHelper());            // add the helper, not the controls object
tc.attach(selectedMesh);
tc.setMode('translate');              // 'rotate' | 'scale'
tc.setSpace('local');                 // or 'world'
tc.setTranslationSnap(0.25); tc.setRotationSnap(THREE.MathUtils.degToRad(15));
tc.addEventListener('dragging-changed', e => { orbit.enabled = !e.value; });
tc.addEventListener('objectChange', () => markDirty(selectedMesh));
```
TransformControls extends `Controls` rather than `Object3D`, so its visual is the object returned by `getHelper()`.

## 2. Selection
Raycast on `pointerdown` to choose the object, but ignore clicks while `tc.dragging` is true,
and ignore hits on the gizmo itself (the helper is in the scene).

## 3. DragControls
```js
import { DragControls } from 'three/addons/controls/DragControls.js';
const dc = new DragControls(draggables, camera, renderer.domElement);
dc.addEventListener('dragstart', () => orbit.enabled = false);
dc.addEventListener('dragend', () => orbit.enabled = true);
dc.addEventListener('drag', e => { e.object.position.y = 0; });   // constrain to ground plane
```
DragControls moves objects on a plane facing the camera; constrain in the `drag` handler.
`dc.recursive` (default true) controls whether children are picked. By default the left and middle buttons pan the
object and the right button rotates it (`mouseButtons`, `rotateSpeed`).

## Gotchas
- Both controls fight OrbitControls unless you disable orbit during drags.
- Undo: snapshot `object.matrix` on `mouseDown`, push a command on `mouseUp`.

## Verify
- [ ] Dragging the gizmo never orbits the camera; snapping values exact.

## Checked

Checked 2026-10-25 against three.js r186 (npm 0.186.0), TransformControls.js and DragControls.js source.
Confirmed: `getHelper()` returns the root object to add to the scene; `setMode`, `setSpace`, `setTranslationSnap`,
`setRotationSnap`; property changes dispatch `<name>-changed` events (so `dragging-changed`) and `objectChange`, `mouseDown`,
`mouseUp` exist; DragControls events `dragstart`, `drag`, `dragend`, `recursive` default true, drag plane faces the camera,
and default `mouseButtons`.

Method: documentation only; no commands were run.
