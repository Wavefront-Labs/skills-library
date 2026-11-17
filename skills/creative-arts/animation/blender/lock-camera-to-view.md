---
id: creative-arts.animation.blender.lock-camera-to-view
name: lock-camera-to-view
category: creative-arts
field: animation
product: blender
tags: [blender, camera, lock-camera-to-view, fly-navigation, walk-navigation, camera-placement]
level: practitioner
status: docs-checked
description: "Place cameras interactively in Blender: Lock Camera to View, align active camera to view, fly and walk navigation keys, and recording camera moves."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/navigate/walk_fly.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/sidebar.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/navigate/camera_view.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lock-camera-to-view

Goal: frame shots by navigating like an operator instead of typing transforms.

## Lock Camera to View
N panel > View > **View Lock** > **Camera to View**: in camera view (Numpad 0), navigating the viewport moves the camera instead of the view. The lock can also be toggled from the navigation gizmo. Turn it off after framing to avoid accidental moves.

## Align to view
**Align Active Camera to View** (operator view3d.camera_to_view) aligns the active camera to match the current 3D view. **Frame Camera Bounds** (Home) and **Zoom Camera 1:1** help check the framing; the camera view menu is View > Cameras.

## Fly / Walk
View > Navigation > **Walk Navigation** or **Fly Navigation** (Shift+` starts the one configured in Preferences > Navigation).
- Walk: W/A/S/D move, E/Q up/down only while Gravity is off, mouse look, Shift fast, Alt slow, Tab toggles **Gravity**, V jumps (Gravity on), Space teleports to the crosshair, wheel or numpad +/- adjusts speed, LMB confirms, RMB/Esc cancels and restores.
- Fly: W/A/S/D and E/Q accelerate, wheel or numpad +/- changes acceleration, MMB pans, Alt slows, LMB confirms, Esc/RMB cancels.
When started from camera view, the camera moves with you.

## Recording moves
Enter camera view, enable Auto Keying, start animation playback, then activate Fly/Walk: the path is recorded as camera keyframes. Playback cannot be controlled while navigating, so exit with LMB before stopping playback. Clean up the curves in the Graph Editor.

## Gotchas
- Walk mode with Gravity on in a scene without a floor keeps falling; toggle Gravity with Tab.

## Verify
Disable lock, orbit: camera stays put; check camera transform keys exist if recording.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), editors/3dview/navigate/camera_view (Align Active Camera to View, Lock Camera to View, Frame Camera Bounds), walk_fly (key tables, recording procedure), sidebar (View Lock > Camera to View). Removed unconfirmed Ctrl+Alt+Numpad0 shortcut, Camera to Selected, ortho-scale zoom claim and Walk preference names.
Method: documentation only; no commands were run.
