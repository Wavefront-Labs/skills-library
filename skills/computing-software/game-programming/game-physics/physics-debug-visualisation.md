---
id: computing-software.game-programming.game-physics.physics-debug-visualisation
name: physics-debug-visualisation
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, physics-debug-draw, debug-visualization, contact-points, pvd, chaos-visual-debugger, physics-debugging, game-programming]
level: practitioner
status: verified
description: "Debug physics visually: drawing colliders, contacts, normals, joints, sleep state and broadphase bounds, engine viewers (PhysX PVD, Chaos Visual Debugger, Jolt), and recording."
sources: ["https://box2d.org/documentation/", "https://github.com/jrouwe/JoltPhysics", "https://docs.unity3d.com/Manual/PhysicsDebugVisualization.html", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/OmniVisualDebugger.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Physics debug visualisation

**Goal:** see what the solver sees: most physics bugs (wrong collider, flipped normal, missing
contact, wrong layer) are obvious when drawn and invisible otherwise.

## What to draw (and colour conventions)
| Item | Draw | Tells you |
|---|---|---|
| Collider shapes | wireframe; colour by state: awake (green), sleeping (grey), kinematic (blue), static (dark) | collider vs mesh mismatch, sleep bugs |
| Contact points | dot + normal arrow scaled by impulse | flipped normals, missing contacts, ghost collisions on edges |
| Penetration | line of depth length | solver not resolving, slop too high |
| Joints | anchors, axes, limit arcs | wrong anchor frames |
| Centre of mass + inertia axes | small triad | lopsided cars, odd spinning |
| Velocity | arrow | tunnelling candidates |
| Broadphase AABBs / BVH | boxes per level | fat AABB sizes, too many pairs |
| Queries | ray/shape casts with hit point | gameplay raycasts with wrong layer masks |
Implement with a callback interface (Box2D `b2DebugDraw` struct of callbacks, Bullet `btIDebugDraw`, Jolt `DebugRenderer`)
that your renderer implements with an immediate-mode line batcher (see game-engine-architecture
`debug-drawing-system`).

## Engine tools
- **PhysX:** OmniPVD (successor of the PhysX Visual Debugger) records PhysX simulations to a file or stream and a viewer
  reads them back; PhysX also has built-in debug visualization (`DebugVisualization` docs page).
- **Unity:** Physics Debugger window (Window > Analysis > Physics Debugger); tabs Info, Filtering, Rendering, Contacts and Queries,
  drawn in the Scene view.
- **Godot:** Debug > Visible Collision Shapes (and Visible Navigation) in the editor run menu.
- **Jolt:** build with `JPH_DEBUG_RENDERER`; `BodyManager::DrawSettings`; `DebugRendererRecorder` output opens in the JoltViewer app.

## Workflow
1. Reproduce with simulation recording on (OmniPVD or Jolt recorder capture, or your own state log).
2. Pause and single-step (fixed dt) on the problem frame.
3. Toggle categories one at a time; filter to the selected body so the screen stays readable.
4. Compare the collider to the render mesh first: most "physics bugs" are authoring bugs.

## Verify
- [ ] One key toggles physics draw in dev builds; draw code is stripped from shipping.
- [ ] Contact normals and impulses draw for the selected body.
- [ ] Physics frames can be recorded and replayed after a bug happens.

## Checked (2026-10-22)
- Unity manual 'PhysicsDebugVisualization' page: 'go to Window > Analysis > Physics Debugger' (fetched; tab names from the manual via search). Godot docs source: 'Visible Collision Shapes' under the Debug menu.
- PhysX 5.4.1 OmniVisualDebugger page (OmniPVD records and reads back simulations, successor of PVD) and DebugVisualization page. Jolt master: `JPH_DEBUG_RENDERER` in `Core.h`/`Jolt.cmake`, `BodyManager::DrawSettings` (struct at `BodyManager.h:243`), `Jolt/Renderer/DebugRenderer.h`, JoltViewer includes `DebugRendererPlayback`. Box2D main: `b2DebugDraw` struct in `types.h`. The cross-referenced skill `debug-drawing-system` exists.
- Removed the Unreal console variables, `show Collision`, `pxvis collision` and the Chaos Visual Debugger bullet (Epic's pages render no text for fetching), and the claim that PVD connects over a socket.
- The colour table is a convention suggestion, not a checkable claim.
