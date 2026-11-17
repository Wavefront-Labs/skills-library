---
id: creative-arts.animation.blender.camera-dolly-crane
name: camera-dolly-crane
category: creative-arts
field: animation
product: blender
tags: [blender, camera-animation, camera-dolly, dolly, camera-track-move, crane-rig, camera-rigs-addon, dolly-rig]
level: practitioner
status: docs-checked
description: "Animate real-world camera moves in Blender: dolly/track on a path via Follow Path Offset Factor, aim empties, and the Add Camera Rigs extension (Dolly, Crane, 2D)."
sources:
  - https://docs.blender.org/manual/en/latest/animation/constraints/relationship/follow_path.html
  - https://extensions.blender.org/add-ons/add-camera-rigs/
  - https://github.com/waylow/add_camera_rigs
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# camera-dolly-crane

Goal: camera moves that feel physically operated, not floaty free-camera keys. Shot design is in `camera-cinematography`.

## Dolly / track on a path

- Select the camera, add the curve to the selection, press `Ctrl P` and choose *Path Constraint* for a quick Follow Path setup.
- Enable *Fixed Position* and animate **Offset Factor** (0 is the start of the curve, 1 the end). Despite the name, the owner still moves over time when Offset Factor is animated. Without Fixed Position, *Offset* is a frame count subtracted from the curve's Evaluation Time.
- The constraint uses the owner's world position and rotation as offsets on the curve. For a perfectly aligned owner, clear them first with `Alt G` and `Alt R`.
- *Follow Curve* rotates the owner using *Forward Axis* and *Up Axis*; these must differ or the constraint stops working and its icon turns red. Leave Follow Curve off if you want to aim separately.
- Combine Follow Path with a tracking constraint (for example Track To an empty) to keep the moving camera pointed at an object.
- Separate the moves: path = translation, aim empty = pan/tilt, focal length = zoom. Each on its own curve, easier to polish. Ease the Offset Factor keys (see `clamp-to-follow-path`).

## Add Camera Rigs (extension)

- Install from Preferences, Get Extensions, search "Add Camera Rigs". It adds Dolly Rig, Crane Rig and 2D Camera Rig to the Add > Camera menu; the rig is built at the 3D cursor with a new camera that becomes the active scene camera.
- **Dolly Rig / Crane Rig** controls: *Root* (parent of the whole rig), *Camera* (translates the camera; tracks to Aim by default), *Camera_Offset* (child for extra rotation or translation), *Aim* (the camera points at it; rotate it on its Y axis to tilt the camera).
- The Crane Rig adds *Crane_Height* and *Crane_Arm* (arm length) controls; scale them or use the sliders in the UI (both default to 1 unit, both animatable) to get arcing boom moves.
- **2D Camera Rig**: for mostly static shots where the action happens in front of the camera; you frame by moving *Left_corner* and *Right_corner* and the camera adapts its settings. If Aim tracking or the 2D rig do not work, check "Auto Run Python Scripts" in Preferences, Save & Load.
- UI panel: 3D Viewport, Sidebar, Item, Camera Rig. It has Focal Distance, F-Stop and Focal Length (custom properties on the camera control bone, animatable inside the armature), *Set DOF to Aim*, *Set Dolly Zoom*, *Shift To Pivot* (useful for turnarounds), *Swap Lens*, *Lens Breathing*, *Tracking (Aim Lock)*, *Lock Camera Select* and *Add Marker and Bind* for camera switching on Timeline markers.

## Verify

Motion path on the camera shows a smooth curve with eased spacing; playback reads like an operated move.

## Checked

2026-11-09. Confirmed against the Blender manual Follow Path Constraint page (raw RST) and the Add Camera Rigs README (extensions page and GitHub). Removed unconfirmed claims: real-world dolly speeds and ease durations, "heading/pitch" crane controls, the add-on being bundled (it is an extension), and the Euler-keys-versus-Track-To and path-length gotchas.
Method: documentation only; no commands were run.
