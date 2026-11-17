---
id: computing-software.game-programming.unity.charactercontroller-move-slopes-and-steps
name: charactercontroller-move-slopes-and-steps
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, unity-charactercontroller, slope-limit, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity's CharacterController: Move semantics (no gravity, CollisionFlags), Slope Limit, Step Offset, Skin Width, Min Move Distance, and OnControllerColliderHit."
sources: ["https://docs.unity3d.com/Manual/class-CharacterController.html", "https://docs.unity3d.com/ScriptReference/CharacterController.Move.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CharacterController Move, slopes and steps

**Goal:** drive a capsule character with Unity's built-in Character Controller without Rigidbody physics.

## What it is
A capsule-shaped collider you tell to move from a script. It is constrained by collisions: slides along
walls, walks up stairs lower than Step Offset and on slopes within Slope Limit. It does not react to
forces and does not automatically push Rigidbodies. To push things, apply forces to what it collides with
in `OnControllerColliderHit()`. It cannot be affected by objects through physics. If the player should be
affected by physics, the manual suggests a Rigidbody instead.

## Properties
- **Slope Limit**: only climbs slopes less steep (degrees) than the value. The manual says it should not
  be too small and that often 90 degrees works best; the capsule shape stops it climbing walls.
- **Step Offset**: steps up a stair only if closer to the ground than this value. Must not be greater than
  the controller's height or it generates an error. For a 2 m human the manual says to keep it between
  0.1 and 0.4.
- **Skin Width**: colliders can penetrate each other up to it. Larger reduces jitter; too low can cause
  sticking. Manual: a good setting is 10% of Radius; elsewhere "at least greater than 0.01 and more than
  10% of the Radius".
- **Min Move Distance**: movement below it does not happen at all; leave at 0 in most situations.
- **Center** offsets the capsule in world space without affecting the pivot; **Radius**; **Height**
  (about 2 m recommended for a human-like character).
- Layer Overrides: Layer Override Priority, Include Layers, Exclude Layers.

## Move
`public CollisionFlags Move(Vector3 motion)` (`UnityEngine.PhysicsModule`).
- Takes absolute movement delta values; collisions constrain it.
- Returned `CollisionFlags` indicates collision direction: None, Sides, Above, Below.
- It does not use gravity, so apply your own. The page example reads `controller.isGrounded`, keeps
  `velocity.y` at -2 when grounded (comment: slight downward velocity to keep grounded stable), sets a
  jump velocity `Mathf.Sqrt(jumpHeight * -2f * gravityValue)`, adds `gravityValue * Time.deltaTime`, and
  calls `controller.Move(finalMove * Time.deltaTime)` once per `Update`.

## Hints from the manual
- Changing properties in the Inspector recreates the controller, so existing Trigger contacts are lost and
  no OnTriggerEnter messages arrive until the controller moves again.
- The capsule used in queries such as raycast might shrink by a small factor, so queries can miss in
  corner cases even when they appear to hit the gizmo.

## Checked
Date: 2026-11-07

Read in full: the Character Controller component reference and the `CharacterController.Move` page
including its Input System example.

Removed because the pages do not confirm it: the "keep Step Offset below radius" claim, the claim that
the controller ignores other Collider components on itself, `isGrounded` reflecting only the last Move
and flickering on downhill slopes, the SphereCast snap, sliding down steep slopes via `hit.normal`, the
`SimpleMove` remarks, the teleport recipe and Auto Sync Transforms, the AddForceAtPosition push code and
the Verify list. The manual's skin width text appears in two forms (10% of Radius, and "more than 10%"),
both quoted.

Method: documentation only; no commands were run.
