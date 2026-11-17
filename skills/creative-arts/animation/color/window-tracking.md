---
id: creative-arts.animation.color.window-tracking
name: window-tracking
category: creative-arts
field: animation
product: color
tags: [window-tracking, secondary-grading, tracker, cloud-tracker, point-tracker, frame-mode, keyframes, davinci-resolve, grading]
level: practitioner
status: draft
description: "Make Resolve windows follow moving characters and camera moves: cloud vs point tracking, tracked parameters, fixing drift with frame mode keyframes."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.blackmagicdesign.com/products/davinciresolve/training
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking windows

**Goal:** a window that stays glued to its subject through motion.

## Procedure (Resolve Tracker palette, Window mode)

1. Place the window on the subject at a frame where it is clearly visible (often the middle).
2. Choose tracked parameters: Pan, Tilt, Zoom, Rotate, 3D (perspective). Turn off what is not
   happening (a pan-only camera move: Pan and Tilt only) to avoid jitter.
3. **Cloud tracker** (default): tracks texture inside the window. **Point tracker**: add specific
   points on high-contrast features. Use point tracking for flat animation, which has little
   texture inside shapes for a cloud tracker to lock onto.
4. Track forward and backward from the placed frame.
5. Inspect the track graph; spikes show slips.

## Fixing slips

- **Frame mode** (Tracker palette option): window position is keyframed by hand instead of tracked.
  Use it to correct just the slipping frames: in Frame mode, move the window on a bad frame and the
  tracker interpolates.
- Interactive mode: exclude moving foreground from the track area so the tracker ignores occluders.
- Re-track a short section by selecting a range.

## Animation notes

- Flat-shaded characters on flat backgrounds track poorly with clouds; track the line art edges
  with points, or track the background for camera moves and keyframe the character.
- For CG, a better source is a matte/ID pass from render: no tracking, perfect edges.
- Limited animation with holds: one keyframe per pose (Frame mode) is often faster than tracking.

## Gotchas

- Track data lives on the node; copying the grade to another clip copies the track (usually wrong).
  Use "Copy track data" deliberately or re-track.
- Changing the window shape after tracking keeps the track; changing clip in/out points may
  invalidate it.

## Verify

Play the shot at speed with Highlight on (or with the window outline shown): no visible lag,
float or jump of the window relative to the subject.
