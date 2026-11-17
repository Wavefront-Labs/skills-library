---
id: computing-software.game-programming.unity.transform-hierarchy-and-spaces
name: transform-hierarchy-and-spaces
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-gameobject, unity-transform-hierarchy, local-vs-world-space, setparent, transformpoint, quaternion, lossyscale, hierarchy-performance, game-programming]
level: intro
status: docs-checked
description: "Work with Unity Transforms: local vs world position/rotation, SetParent worldPositionStays, TransformPoint/Direction and the world and local property pairs."
sources: ["https://docs.unity3d.com/ScriptReference/Transform.html", "https://docs.unity3d.com/ScriptReference/Transform.SetParent.html", "https://docs.unity3d.com/ScriptReference/Transform.TransformPoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transform hierarchy and coordinate spaces

**Goal:** place, attach and move objects without off-by-a-parent bugs.

Every object in a Scene has a Transform storing position, rotation and scale. Every Transform can have a parent, which applies position, rotation and scale hierarchically (the Hierarchy pane). A Transform can be enumerated to loop over its children with `foreach (Transform child in transform)`.

## Local vs world
| Property | Space |
|---|---|
| `position`, `rotation` (a Quaternion), `lossyScale` (read-only global scale) | World. |
| `localPosition`, `localRotation`, `localScale`, `localEulerAngles` | Relative to the parent. |
| `forward` (blue axis), `right` (red), `up` (green) | Normalized world-space directions of the axes. |
| `localToWorldMatrix`, `worldToLocalMatrix` | Read-only matrices converting points between local and world space. |

`GetPositionAndRotation` and `GetLocalPositionAndRotation` read both in one call; `SetPositionAndRotation` (world) and `SetLocalPositionAndRotation` (local) set both in one call.

## Converting between spaces
```csharp
Vector3 muzzleWorld = gun.TransformPoint(new Vector3(0, 0, 0.8f)); // local point -> world, affected by scale
Vector3 aimWorld    = gun.TransformDirection(Vector3.forward);     // local direction -> world
Vector3 offsetWorld = gun.TransformVector(Vector3.forward);        // local vector -> world
Vector3 local       = body.InverseTransformPoint(hit.point);       // world point -> local
```
- `TransformPoint` result is affected by scale; use `TransformDirection` for direction vectors.
- For many points at once, `TransformPoints` is much faster than repeated `TransformPoint` calls. Plural variants exist for directions and vectors, and for the inverse conversions.

## Parenting
```csharp
item.SetParent(handSocket, worldPositionStays: false); // keep local values, move with the new parent
item.SetParent(null);                                  // unparent: becomes a top-level object
```
- `SetParent` is the same as the `parent` property except that it can keep the Transform's local orientation instead of its global one.
- `worldPositionStays` defaults to true: the parent-relative position, scale and rotation are modified so the object keeps the same world position, rotation and scale. With false, the object keeps its local values and so appears in the same place relative to the new parent (for example next to it, as it was next to the old parent).

## Checked
Method: 2026-11-09 docs-only read of the Transform class page (properties and methods table), Transform.SetParent (both overloads, remarks) and Transform.TransformPoint (Vector3 overload) script reference pages. Removed claims not on those pages: eulerAngles flipping and the Quaternion.Euler advice, non-uniform-scale skew, the whole performance section (TransformAccessArray, deep-hierarchy cost, one-update setters, caching transform) and the Verify list.
