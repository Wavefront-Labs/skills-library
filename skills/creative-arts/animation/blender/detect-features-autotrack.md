---
id: creative-arts.animation.blender.detect-features-autotrack
name: detect-features-autotrack
category: creative-arts
field: animation
product: blender
tags: [blender, motion-tracking, detect-features, auto-track, camera-tracking]
level: practitioner
status: docs-checked
description: "Seed many tracks with Detect Features in the Blender Movie Clip Editor: Placement, Margin, Threshold and Distance, annotation areas, then track and clean up bad tracks."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# detect-features-autotrack

Goal: a large set of tracks for a camera solve without placing each by hand.

## Detect Features (Track menu, or toolbar Track tab > Marker)

It detects features on the **current frame only** and places markers on them. It does not take other frames into account, so it may mark features on moving objects. Options (Adjust Last Operation panel):

- **Placement**: Whole Frame, Inside Annotated Area, Outside Annotated Area (use the Annotate tool to outline areas of interest or areas to avoid, such as people or trees).
- **Margin**: distance from the image boundary (default 16 pixels in the 5.2 source). Markers too close to the edge fail quickly.
- **Threshold**: minimum feature quality from the detection algorithm (default 0.5); it controls how many markers are added.
- **Distance**: minimum distance between placed markers (default 120 pixels); markers too close together can confuse the solver.

## Workflow

1. Go to a frame where the static background is clearly visible and run Detect Features.
2. Select the markers and track forward (Ctrl T), then backward (Shift Ctrl T) if the clip starts earlier.
3. Run it again on later frames as earlier tracks end.
4. Clean up with Track > Clean Up > **Clean Tracks** (Tracked Frames, Reprojection Error, Action) and **Filter Tracks**, and delete tracks on moving objects.
5. A solve needs at least eight common tracks on both solve keyframes (see `creative-arts.animation.blender.solve-keyframes`).

## Gotchas

- Markers on moving things (people, vegetation, water) ruin camera solves: exclude them with an annotation or delete them.
- Markers at occlusion edges where objects at different depths meet are not real 3D points (practice, not from the manual).

## Verify

Scrub the clip: each frame keeps enough healthy tracks spread over the frame, and the solve error is acceptable.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/editing/track) and the 5.2 source (tracking_ops_detect.cc property defaults and labels, blender_default keymap). Fixed: the option is called Distance in the UI, it detects on the current frame only, and the menu is Track > Detect Features. Removed unconfirmed claims: annotation shortcut D, a 30 to 80 marker target, the claim that lower thresholds give more features, motion-blur advice and per-frame count bars.
Method: documentation only; no commands were run.
