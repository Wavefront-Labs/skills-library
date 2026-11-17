---
id: computing-software.game-programming.gameplay-programming.top-down-and-twin-stick-movement
name: top-down-and-twin-stick-movement
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, twin-stick, top-down-movement, aim-direction, mouse-aim, camera-relative-input, diagonal-normalization, game-programming]
level: practitioner
status: draft
description: "Implement top-down and twin-stick controls: normalized 8-way movement, camera-relative input, separate aim from right stick or mouse ray, aim smoothing, and wall sliding."
sources: ["https://docs.unity3d.com/ScriptReference/Plane.Raycast.html", "https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-get-vector", "https://www.gdcvault.com/play/1020779/Juice-It-or-Lose"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Top-down and twin-stick movement

**Goal:** responsive top-down movement with independent aiming that works with gamepad and mouse.

## Movement
```
move = read_vector(left_stick or WASD)              # radial dead zone already applied
if |move| > 1: move = normalize(move)               # keyboard diagonals would be 1.41x faster
move = camera_relative(move)                        # for angled 3D cameras
velocity = move_towards(velocity, move * maxSpeed, accel * dt)
```
Camera-relative input for a tilted/rotated camera:
```
fwd   = normalize(project_on_plane(camera.forward, up))
right = normalize(project_on_plane(camera.right, up))
world = right * move.x + fwd * move.y
```
Keyboard: digital inputs give 8 directions; for analog sticks keep magnitude for walk/run blending.

## Aim
- **Gamepad**: aim = right stick direction when above a dead zone (~0.3); otherwise keep last aim (or
  fall back to movement direction). Optional aim smoothing (rotate toward target angle at a max deg/s)
  and aim assist (bias toward nearby targets within a cone).
- **Mouse**: cast a ray from the camera through the cursor onto the ground plane at the character's
  height:
```csharp
var plane = new Plane(Vector3.up, new Vector3(0, transform.position.y + aimHeight, 0));
Ray ray = cam.ScreenPointToRay(Mouse.current.position.ReadValue());
if (plane.Raycast(ray, out float t)) aimDir = (ray.GetPoint(t) - transform.position).WithY(0).normalized;
```
  Use a plane at weapon height, not the terrain, so aim does not jump on uneven ground.
- Switch input mode automatically on last device used; show a cursor/reticle only for mouse.

## Facing and animation
Body faces aim direction (strafe animations driven by movement relative to facing:
`local = inverse(rotation) * velocity`), or faces movement when not aiming. Blend spaces on local X/Y.

## Collisions
Kinematic controllers: slide along walls (collide-and-slide / `move_and_slide`) so diagonal input into
a wall keeps moving along it instead of stopping dead. Slightly round collision shapes (circles/capsules)
avoid snagging on tile corners.

## Feel extras
Dash with brief i-frames, recoil pushback on firing, screen shake scaled by weapon; small acceleration
times (~0.05 s) keep it snappy.

## Verify
- [ ] Diagonal speed equals cardinal speed with keyboard input.
- [ ] Mouse aim stays correct on slopes and with a tilted camera.
- [ ] Switching between mouse and gamepad mid-play switches aim mode without jumps.
