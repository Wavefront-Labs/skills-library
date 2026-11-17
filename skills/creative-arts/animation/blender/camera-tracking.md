---
id: creative-arts.animation.blender.camera-tracking
name: camera-tracking
category: creative-arts
field: animation
product: blender
tags: [blender, camera-tracking, motion-tracking, camera-solve, tracking, matchmove, movie-clip-editor, solve-error, lens-distortion, tripod-solve, set-scene, footage-integration]
level: advanced
status: docs-checked
description: "Matchmove in Blender's Movie Clip Editor: camera data, 2D tracks, solving with keyframes and refine, solve error, orientation and scale, Setup Tracking Scene and lens distortion."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/introduction.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/track.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/camera.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# camera-tracking

Goal: a solved 3D camera and point cloud so CG sits in live footage with a low solve error.

## Footage and camera data

- Open the clip in the Movie Clip Editor (Clip > Open Clip, Alt O). **Clip > Set Scene Frames** sets the scene end frame to match the clip duration. Prefetch (P) fills the cache; see `creative-arts.animation.blender.clip-proxies-prefetch`.
- Sidebar > Track tab > **Camera** panel (presets in the panel header; distortion coefficients and optical centre are not in the presets): **Sensor Width** (from the camera specification), **Pixel Aspect**, **Focal Length** (mm or pixels), **Optical Center** (normalised image coordinates), **Lens Distortion** model (Polynomial K1 to K3, Division K1 K2, Nuke K1 K2, Brown K1 to K4 plus P1 P2).

## Placing and tracking markers

- Ctrl LMB places a marker on the footage. A marker has a pattern area and a search area.
- **Tracking Settings** (toolbar Track tab, or Sidebar for the active track): Pattern Size and Search Size (defaults 21 and 71 pixels), **Motion Model** (Location, Location & Rotation, Location & Scale, Location Rotation & Scale, Affine, Perspective), **Match** (Keyframe or Previous Frame), **Prepass**, **Normalize**, R/G/B channels, plus Weight, Correlation (default 0.75), Margin, Frames Limit and Speed under the extra settings. *Copy from Active Track* copies settings to the defaults.
- Track Motion: Ctrl T forward, Shift Ctrl T backward, Alt Right and Alt Left one frame. If the algorithm fails during sequence tracking the marker is disabled and tracking continues for the rest.
- **Detect Features** (Track menu) places markers on the current frame only: Placement (Whole Frame, Inside or Outside Annotated Area), Margin, Threshold, Distance. It ignores other frames, so it can mark moving objects. See `creative-arts.animation.blender.detect-features-autotrack`.
- Clean Up: **Clean Tracks** (Tracked Frames, Reprojection Error, Action: Select, Delete Track, Delete Segments) and **Filter Tracks**. Join Tracks is Ctrl J.

## Solving (toolbar Solve tab)

- Requirements from the manual: at least eight common tracks on both solve keyframes, and noticeable parallax between them.
- **Keyframe** (automatic selection) or **Keyframe A/B**; **Tripod** for cameras that only rotate; **Refine** with Focal Length, Optical Center, Radial Distortion, Tangential Distortion. You still need approximate initial values for refine to work.
- **Solve Camera/Object Motion** reports the average reprojection error in the editor header. The manual reads below 0.3 as accurate, 0.3 to 3.0 as usable, and above 3 as a sign of tracks to improve or wrong focal length or distortion values.

## Orientation and scale

Reconstruction menu or Solve > Orientation panel: **Set Origin** (active track to the origin, translation only), **Floor** (three selected tracks to Z = 0), **Wall**, **Set X/Y Axis**, **Set Scale** (distance between two tracks matches the *Distance* field), **Apply Scale** (modifies the tracking data). The camera motion is applied through the **Camera Solver** constraint.

## Scene setup

- **Set as Background** shows the clip as the camera background in visible 3D Viewports.
- **Setup Tracking Scene** (needs a valid solve): see `creative-arts.animation.blender.setup-tracking-scene`.
- **3D Markers to Mesh** (Reconstruction menu) creates a mesh from the solved tracks as a start for manual modelling. **Link Empty to Track** creates Follow Track empties (see `creative-arts.animation.blender.link-empty-to-track`).
- Lens distortion with the Movie Distortion node: the manual recommends distorting the render and leaving the clip alone when the clip bulges out, and undistorting the clip when it bulges in, because the wrong choice needs pixels Blender does not have and gives edge artefacts. See `creative-arts.animation.blender.lens-distortion-undistort`.

## Verify

- The header solve error is acceptable and every frame has enough tracks.
- A test object on the floor (Setup Tracking Scene makes a cube and a ground plane) does not slide against the footage across the shot.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/*) and the 5.2 source (space_clip.py panels and menus, blender_default keymap for the clip editor, tracking.cc defaults, tracking_ops_detect.cc, bl_operators/clip.py). Fixed: solve-error thresholds (manual: 0.3 and 3.0, not 0.3 and 1), the eight-track requirement applies to both keyframes, Set Scene Frames only sets the end frame and is not in a Footage Settings panel, Setup Tracking Scene does not set Film Transparent, the Camera panel has no sensor presets list of values. Removed unconfirmed: ffmpeg conversion, sensor sizes, per-frame track counts, shadow catcher in EEVEE, tripod scale notes, rolling shutter and zoom remarks.
Method: documentation only; no commands were run.
