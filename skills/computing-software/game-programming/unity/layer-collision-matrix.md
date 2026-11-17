---
id: computing-software.game-programming.unity.layer-collision-matrix
name: layer-collision-matrix
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, layer-collision-matrix, physics-layers, layer-overrides, game-programming]
level: intro
status: docs-checked
description: "Use the Unity Layer Collision Matrix to choose which layers collide, and Physics.IgnoreLayerCollision to change pairs at runtime, including its trigger-reset side effect."
sources: ["https://docs.unity3d.com/Manual/LayerBasedCollision.html", "https://docs.unity3d.com/ScriptReference/Physics.IgnoreLayerCollision.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer collision matrix

**Goal:** decide which GameObjects can collide by layer instead of filtering in collision callbacks. Unity 6000.x docs.

## Set it up
1. Select a GameObject, open the **Layer** dropdown at the top of the Inspector, and choose a layer or add a new one.
   Repeat for each GameObject.
2. Edit > Project Settings > **Physics**.
3. In the **Layer Collision Matrix**, tick the layer pairs that should interact.

The matrix defines which GameObjects can collide with which layers. Example from the page: to let Layer 1 collide with
Layers 2 and 3 but not Layer 1, find the Layer 1 row, tick the Layer 2 and Layer 3 columns, and leave the Layer 1 column
unticked.

## Change pairs at runtime
```csharp
// Signature: public static void IgnoreLayerCollision(int layer1, int layer2, bool ignore)
Physics.IgnoreLayerCollision(layer1, layer2, true);
```
- Makes the collision detection system ignore all collisions between any collider in `layer1` and any collider in
  `layer2`.
- It resets the trigger state of affected colliders, so you may receive `OnTriggerExit` and `OnTriggerEnter` messages in
  response to calling it.
- The Physics inspector sets the project defaults for any layer combination.
- Related: `Physics.GetIgnoreLayerCollision`, `Physics.IgnoreCollision`.
- The page's own example calls `Physics.IgnoreLayerCollision(0, 8)` with two arguments, which does not match the three
  parameter signature above; pass the `ignore` flag explicitly.

## Checked
Date: 2026-11-07.
Read in full: "Layer-based collision detection" manual page and the `Physics.IgnoreLayerCollision` script reference
(6000.6 docs). The linked Tags and layers, Collision detection and Layers pages were not opened.
Removed as unconfirmed: the layer naming scheme and example matrix, the broadphase/performance claims, Physics 2D matrix
separation, collider Layer Overrides (Include/Exclude Layers) and their Unity version, `Physics.IgnoreCollision` usage
detail, runtime `gameObject.layer` changes, raycast `LayerMask` guidance and `Physics.queriesHitTriggers`, the 32-layer
limit and reserved layers, child collider layer behavior, and the invented Verify checklist.
Method: documentation only; no commands were run.
