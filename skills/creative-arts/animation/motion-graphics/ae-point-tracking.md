---
id: creative-arts.animation.motion-graphics.ae-point-tracking
name: ae-point-tracking
category: creative-arts
field: animation
product: motion-graphics
tags: [point-tracking, motion-tracking, after-effects, tracker-panel, track-motion, attach-point, null-object, feature-region, search-region]
level: practitioner
status: draft
description: "Track features with the After Effects point tracker (one/two-point), apply data to a null, size feature and search regions, and repair drifting tracks."
sources:
  - https://helpx.adobe.com/after-effects/using/tracking-stabilizing-motion-cs5.html
  - https://helpx.adobe.com/after-effects/using/tracking-stabilizing-motion.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point tracking in After Effects

**Goal:** a graphic (label, HUD element, sticker) follows a feature in footage or a rendered shot.

## Procedure

1. Select the footage layer, Window - Tracker - **Track Motion** (opens the layer panel).
2. Track type: Transform; tick Position (one point) or Position + Rotation + Scale (two points).
3. Place the track point: inner box (**feature region**) around a high-contrast, distinct feature;
   outer box (**search region**) large enough to contain the feature's motion between frames.
   The cross is the **attach point** (where the target's anchor will land); offset it with Ctrl/Cmd-drag.
4. Options: channel RGB/Luminance/Saturation (pick what gives most contrast), "Adapt feature on
   every frame" for changing features, confidence threshold behaviour.
5. Track forward (and backward from a mid frame if the feature enters later).
6. Create a Null (Layer - New - Null Object), set it as **Edit Target**, Apply (X and Y). Parent
   graphics to the null rather than applying tracks directly to artwork.

## Repairing

- Watch the confidence values (twirl down the track point): drops show slips.
- Stop at the bad frame, move the feature box back onto the feature, and continue tracking from there.
- For occlusions, track up to the occlusion, skip ahead, re-position, continue; keyframes in between
  interpolate.
- Smooth jitter: The Smoother (Window - Smoother) on the null's position, or a small `smooth()` expression.

## Rendered animation tips

- Prefer exporting the transform from the 3D/2D animation app (camera or null data) instead of
  tracking renders: exact and drift-free.
- Flat colour areas have no texture: track line-art corners and intersections, or use two-point
  tracking on outline features.

## Gotchas

- Tracking a scaled/rotated precomp layer tracks in the layer's space; apply to a target in the same
  comp or the null ends up offset.
- Motion blur smears features; track the unblurred version if available and apply to the final.

## Verify

Play back with the graphic attached at 100%: no slipping on the feature through the whole range,
including frames with motion blur.
