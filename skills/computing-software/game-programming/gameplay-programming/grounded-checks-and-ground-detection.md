---
id: computing-software.game-programming.gameplay-programming.grounded-checks-and-ground-detection
name: grounded-checks-and-ground-detection
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, ground-check, coyote-time, ground-normal, game-programming]
level: practitioner
status: draft
description: "Implement robust grounded checks: sphere/capsule casts vs contact normals, ground layers, edge cases on ledges and slopes, coyote time hooks and debug drawing."
sources: ["https://docs.unity3d.com/ScriptReference/Physics.SphereCast.html", "https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html#class-characterbody2d-method-is-on-floor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grounded checks and ground detection

**Goal:** a single, reliable `isGrounded` (plus ground normal, ground object, time since grounded)
that every gameplay system trusts.

## Methods
| Method | Pros | Cons |
|---|---|---|
| Built-in (`CharacterController.isGrounded`, Godot `is_on_floor()`, UE `IsMovingOnGround`) | free, consistent with movement | only valid after a move; flickers on bumps/slopes |
| Single raycast down | cheap, precise normal | misses on ledges (ray off the edge while capsule still standing) |
| Sphere/capsule cast down | handles ledges | normal at edges is diagonal |
| Contact normals from collisions | exact | engine-specific, one frame late |

Robust default: **sphere cast** from slightly above the capsule bottom, radius a bit smaller than the
capsule, distance = skin + small tolerance, layer-masked to ground layers. Use a **separate ray** from
the center for the slope normal when available.

```csharp
bool CheckGround(out RaycastHit hit) {
    Vector3 origin = transform.position + Vector3.up * (radius + 0.05f);
    bool ok = Physics.SphereCast(origin, radius * 0.95f, Vector3.down, out hit,
                                 0.05f + groundTolerance, groundMask, QueryTriggerInteraction.Ignore);
    return ok && Vector3.Angle(hit.normal, Vector3.up) <= maxSlope && verticalVelocity <= 0.01f;
}
```
Note `verticalVelocity <= small` so the first frames of a jump aren't "grounded".

## State to expose
- `grounded`, `groundNormal`, `groundCollider` (for moving platforms, footstep surface type),
- `timeSinceGrounded` (coyote time), `timeSinceJumpPressed` (jump buffer),
- `justLanded` event with landing speed (camera dip, landing animation, fall damage).

## Edge cases
- Steep slopes: hit but not walkable -> not grounded (slide state).
- Triggers: always ignore (`QueryTriggerInteraction.Ignore` / exclude Area nodes).
- Self-collision: exclude own colliders via layer mask.
- Moving platforms going down: ground snapping (see step-down) so the check doesn't fail each frame.
- Thin ledges: sphere cast succeeds with the character hanging mostly off; decide whether to allow
  (generous) or push off (ledge slip).

## Debugging
Draw the cast every frame (green grounded, red air) with the hit normal; log transitions with frame
numbers. Most "can't jump" bugs are visible in seconds this way.

## Gotchas
- Order: compute grounded after movement in the same tick, read it in the next input step consistently.
- Fixed vs variable update mismatch causes a grounded flicker per render frame; keep checks in the
  physics tick.

## Verify
- [ ] Stand on a ledge with half the capsule off: behaviour matches design.
- [ ] Jump frame N: grounded false from frame N, landing event once per landing.
