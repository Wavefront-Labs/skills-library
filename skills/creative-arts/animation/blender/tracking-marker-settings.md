---
id: creative-arts.animation.blender.tracking-marker-settings
name: tracking-marker-settings
category: creative-arts
field: animation
product: blender
tags: [blender, motion-tracking, tracking-marker-settings, pattern-size, search-size, motion-model, movie-clip-editor]
level: practitioner
status: docs-checked
description: "Set Blender Movie Clip Editor tracker settings: Pattern and Search Size, Motion Model, Match, Prepass, Normalize, Correlation, Margin, Frames Limit, Weight and channel toggles."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/track.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/sidebar/track/track.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# tracking-marker-settings

Goal: markers that stay on their feature through motion, perspective change and lighting shifts.

## Where

Toolbar (T) > Track tab > **Tracking Settings**: defaults for new tracks, with presets in the panel header (the manual says they are based on experience with real footage). Sidebar (N) > Track tab: settings of the active track. **Copy from Active Track** copies the active track's settings into the defaults.

## Settings

- **Pattern Size**, **Search Size**: size of newly created tracks (defaults 21 and 71 pixels in the 5.2 source). The search area must cover the motion between frames.
- **Motion Model**: Location, Location & Rotation, Location & Scale, Location, Rotation & Scale, Affine, Perspective. Choose the one that matches the feature's real motion. The manual says Perspective is usually for planar features but Affine is often a good enough approximation with more stable tracks.
- **Match**: *Keyframe* matches against the image from the frame where the track was keyframed (prevents sliding from the original position, but can cause small jumps and fail when the feature deforms with camera motion). *Previous Frame* tracks between neighbouring frames (copes with large transformations, but can slide away, so watch it).
- **Prepass**: two-pass tracking: a brute-force location-only pass, then the full motion model. Enabled by default.
- **Normalize**: normalises patterns by their average intensity so they are invariant to illumination changes (for example a marker moving into shadow).
- **R, G, B**: channels used by the tracker; disabling some can raise contrast. The tracker works in grayscale space.
- Extra settings: **Weight** (influence of the track in the solve), **Correlation** (minimum similarity for a successful match, default 0.75; decrease it if tracking stops too early, increase it if tracks slip before stopping), **Margin** (disables a track near the image boundary), **Use Mask** (use an annotation to mask part of the pattern), **Frames Limit** (maximum frames per Track Sequence), **Speed** (Double or Half to add delay so slide-off is noticed earlier).

## Tracking

Ctrl T forward, Shift Ctrl T backward, Alt Right or Alt Left one frame. The Track Preview widget in the Sidebar shows the pattern so you can see sliding and drag the track back.

## Verify

Track a feature through the shot: the Track Preview stays on the same detail, the path is smooth, and the track stops when the feature is hidden.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/toolbar/track, sidebar/track/track) and the 5.2 source (tracking.cc defaults, space_clip.py panels, blender_default keymap). Fixed: the manual does not say Keyframe is better for camera solves, and Perspective is not required for plane tracks (Create Plane Track needs point tracks). Removed unconfirmed claims about pattern size ranges, suggested correlation 0.85 to 0.9 and blue noise.
Method: documentation only; no commands were run.
