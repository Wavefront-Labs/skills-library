---
id: computing-software.game-programming.gameplay-programming.first-person-camera-and-head-bob
name: first-person-camera-and-head-bob
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, follow-camera, head-bob, first-person-camera-craft, view-model, game-programming]
level: practitioner
status: draft
description: "Build a first-person camera: mouse and stick look, pitch clamp, head bob and landing dip tied to movement, FOV kicks, and a separate view-model render."
sources: ["https://docs.godotengine.org/en/stable/tutorials/3d/using_transforms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First-person camera and head bob

**Goal:** responsive, comfortable FPS camera with motion that sells movement without causing nausea.

## Look
```csharp
yaw   += mouseDelta.x * sens;                  // mouse: no deltaTime (delta is already per frame)
pitch -= mouseDelta.y * sens * (invertY ? -1 : 1);
pitch  = Mathf.Clamp(pitch, -89f, 89f);
body.rotation = Quaternion.Euler(0, yaw, 0);   // yaw on the body
head.localRotation = Quaternion.Euler(pitch, 0, 0);  // pitch on the camera pivot
```
- Gamepad: `stick * speed * deltaTime` with response curve and optional acceleration ramp after holding
  near max; separate sensitivity settings for mouse and stick.
- Read raw mouse input (no OS acceleration) and do look in the render update (not fixed step) to avoid
  stutter; apply body yaw to physics in the next tick.

## Head bob
Drive from horizontal speed and a phase that advances with distance travelled (not time), so bob
matches footsteps:
```csharp
phase += horizontalSpeed * Time.deltaTime * bobFrequencyPerMeter * Mathf.PI * 2;
float amp = Mathf.InverseLerp(0, runSpeed, horizontalSpeed) * bobAmount * (grounded ? 1 : 0);
Vector3 bob = new(Mathf.Cos(phase * 0.5f) * amp * 0.5f, Mathf.Sin(phase) * amp, 0);
cameraOffset = Vector3.Lerp(cameraOffset, bob, 1 - Mathf.Exp(-12 * Time.deltaTime));
```
- Vertical bob at 2x horizontal frequency (figure-8), small amplitude (1-3 cm walk, 3-5 cm run).
- Trigger footstep sounds at phase crossings for perfect sync.
- **Accessibility option to disable bob and reduce camera motion.**

## Landing and other motion
- Landing dip: spring-damper on vertical offset, impulse proportional to landing speed.
- FOV kick on sprint (+5-10 degrees, eased), strafe roll (tiny, <2 degrees) — all optional and
  scaled by a "camera motion" setting.

## View model
Weapons/arms on a separate camera or render layer with their own FOV (e.g. 60) so they don't clip into
walls and don't stretch with gameplay FOV changes. Apply sway (lagged rotation from look delta) to the
view model, not the main camera.

## Gotchas
- Applying bob to the camera transform that also does raycasts for shooting shifts aim; shoot from the
  unbobbed head pivot.
- Pitch clamp at exactly 90 causes gimbal flips; clamp at 89.
- Fixed-step camera rotation with high-refresh monitors feels laggy.

## Verify
- [ ] Footstep audio aligns with bob dips at walk and run speeds.
- [ ] Disable-motion setting removes bob, FOV kicks and roll.
