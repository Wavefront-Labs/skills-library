---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-physics-react-three-rapier
name: r3f-physics-react-three-rapier
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, react-three-rapier, rapier, rigid-body, colliders, character-controller]
level: practitioner
status: docs-checked
description: "Add physics to React Three Fiber with @react-three/rapier: RigidBody types, auto and manual colliders, impulses, sensors, collision events and character controllers."
sources: ["https://github.com/pmndrs/react-three-rapier", "https://rapier.rs/docs/user_guides/javascript/getting_started_js", "https://rapier.rs/docs/user_guides/javascript/character_controller"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physics with react-three-rapier

## 1. World and bodies
```jsx
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';
<Canvas>
  <Suspense>                                       {/* rapier WASM loads async */}
    <Physics gravity={[0, -9.81, 0]} debug>
      <RigidBody colliders="hull" restitution={0.3} friction={0.8}>
        <mesh geometry={nodes.Crate.geometry} />
      </RigidBody>
      <RigidBody type="fixed" colliders={false}>
        <CuboidCollider args={[50, 0.5, 50]} position={[0, -0.5, 0]} />  {/* half extents */}
        <mesh receiveShadow><boxGeometry args={[100, 1, 100]} /></mesh>
      </RigidBody>
    </Physics>
  </Suspense>
</Canvas>
```
Auto colliders (`colliders` prop on `RigidBody` or `Physics`): `"cuboid"`, `"ball"`, `"hull"` (ConvexHullCollider), `"trimesh"` (TrimeshCollider); `colliders={false}` disables auto-generation.

## 2. Driving bodies
```jsx
const body = useRef();
body.current.applyImpulse({ x: 0, y: 5, z: 0 }, true);
body.current.setLinvel({ x: 2, y: 0, z: 0 }, true);
body.current.setNextKinematicTranslation(pos);       // kinematic bodies, in useFrame
const p = body.current.translation();                // read position
```
Never set the mesh `position` of a dynamic body each frame; Rapier owns the transform.

## 3. Events and sensors
Collision groups: `collisionGroups={interactionGroups(1, [0, 2])}`. For collision and sensor events see the react-three-rapier README.

## 4. Characters
Use Rapier's `KinematicCharacterController` (`world.createCharacterController(offset)`) and call `computeColliderMovement(collider, desiredMovementVector)` each frame. You provide the movement vector, so add a downward component yourself to emulate gravity (Rapier character-controller guide).

## Gotchas
- Create RigidBodies with the centre of gravity at the centre of the object, otherwise simulation interpolation can misbehave (README note).
- Wrap exactly one `InstancedMesh` in `InstancedRigidBodies` to give each instance its own body.

## Verify
- [ ] `debug` view shows colliders matching meshes.
- [ ] Frame time measured with the expected number of dynamic bodies.

## Checked

2026-10-28. Confirmed in the react-three-rapier README: `Physics` needs a `Suspense` wrapper, `debug` and `gravity` props, `colliders` values (`cuboid`, `ball`, `hull`, `trimesh`, `false`), `interactionGroups`, `InstancedRigidBodies`, `applyImpulse(vector, true)`, centre-of-gravity note. Confirmed in the Rapier JS guides: `createCharacterController(offset)`, `computeColliderMovement`, gravity must be added to the movement vector, `setLinvel`, `setNextKinematicTranslation`.
Removed (not in the fetched pages): body type list, "cuboid is the default", `import.meta.env.DEV`, sensor and collision-event snippet, `ecctrl`, `enabledRotations`, `r3f-perf`, `timeStep="vary"`, trimesh and scale claims, 500-body 60 fps check.

Method: documentation only; no commands were run.
