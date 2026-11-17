---
id: creative-arts.animation.blender.vr-scene-inspection
name: vr-scene-inspection
category: creative-arts
field: animation
product: blender
tags: [blender, stereoscopy, vr-scene-inspection, openxr, vr, headset]
level: practitioner
status: docs-checked
description: "Review Blender scenes in a VR headset with the bundled VR Scene Inspection add-on: OpenXR, Start VR Session, landmarks, location scouting viewfinder."
sources:
  - https://docs.blender.org/manual/en/latest/addons/vr_scene_inspection.html
  - https://docs.blender.org/manual/en/latest/getting_started/configuration/hardware.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vr-scene-inspection

Goal: look at a set or layout at true scale in a headset.

## Requirements

- A headset on an OpenXR-compatible platform. The manual's hardware page lists HTC Vive Cosmos and Focus 3 (developer previews), Monado (Linux, not recommended for general use), Meta Rift and Quest (Windows; Quest needs Oculus Link), SteamVR (Windows, Linux), Varjo and Windows Mixed Reality, with minimum software versions noted there. Check that page for current requirements.
- The **VR Scene Inspection** add-on. The current manual lists it as bundled with Blender (support level Official): Preferences > Add-ons, search "VR Scene Inspection", enable. It is not an extensions.blender.org download.

## Use

1. 3D Viewport Sidebar > **VR** tab > **Start VR Session** (tries to connect to the OpenXR platform). Options: Tracking (Positional, Absolute) and **Use Controller Actions** for default navigation, controller tracking and haptics.
2. **View Settings** control what shows in the headset: Floor, Annotations, Selection, Controllers, Custom Overlays, Object Extras, object type visibility, plus Clip Start/End, View Scale and Fly Speed.
3. **Landmarks** store reusable base viewer poses. Types: Scene Camera, Custom Object, Custom Pose. Buttons include Add VR Landmark, Add from Session, Add Landmark from Camera, Scene Camera to Landmark, Cursor to Landmark and Camera from Landmark. Activate a landmark to change the base pose of the VR view.
4. **Location Scouting**: a virtual director's viewfinder (Location Scouting > Viewfinder) inside the session to adjust focal length, depth of field, focus point and aperture and capture shots. Captured shots can be reviewed in the desktop viewport and turned into cameras or markers.
5. **Action Maps** (Gamepad, controller extensions) and **Viewport Feedback** (Show VR Camera, Show Landmarks, **Mirror VR Session** makes the desktop viewport follow the headset view).
6. Preferences > Navigation > VR Navigation (visible only with the add-on on): Vignette Intensity, Turn Speed, Turn Amount, Snap Turn, Invert Rotation.

## Practice notes

- Set Scene Units correctly; wrong scale is obvious in VR.
- Keep the frame rate high: use Solid shading or reduce scene complexity.
- Editing in VR is limited; the session is for inspection and location scouting.

## Verify

Start a session, check that the floor is at your real floor height and a door looks door-sized.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): addons/vr_scene_inspection.rst (bundled, enable steps, VR tab, session options, landmarks, location scouting, action maps, viewport feedback, VR Navigation preferences) and getting_started/configuration/hardware.rst (OpenXR platforms). Fixed the wrong statement that it became an extension in 4.2. Removed the "Failed to get device information" error text and the Solid/Material Preview shading-choice claim. Method: documentation only; no commands were run.
