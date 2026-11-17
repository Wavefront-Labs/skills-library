---
id: creative-arts.animation.motion-graphics.ae-warp-stabilizer
name: ae-warp-stabilizer
category: creative-arts
field: animation
product: motion-graphics
tags: [warp-stabilizer, motion-tracking, stabilization, after-effects, smooth-motion, no-motion, subspace-warp, crop, stabilize-motion]
level: practitioner
status: draft
description: "Stabilise shaky reference, live-action plates and screen captures with After Effects Warp Stabilizer or the point-based Stabilize Motion; avoid wobble and crop loss."
sources:
  - https://helpx.adobe.com/after-effects/using/stabilize-motion-warp-stabilizer.html
  - https://helpx.adobe.com/after-effects/using/tracking-stabilizing-motion.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Warp Stabilizer and Stabilize Motion

**Goal:** remove unwanted camera shake from footage used as plates, reference, or behind-the-scenes
material, without the jelly wobble that over-stabilisation produces.

## Warp Stabilizer (automatic)

1. Apply Effect - Distort - Warp Stabilizer (analysis starts).
2. **Result**: Smooth Motion (keeps intended moves, removes shake; set Smoothness 5-50%) or No Motion
   (locks the shot; for tripod-intended shots).
3. **Method**: Subspace Warp (default, warps parts of the frame; can wobble), Perspective, Position
   Scale Rotation, Position only. If you see wobble or warping, step down to Perspective or
   Position Scale Rotation.
4. **Framing**: Stabilize, Crop, Auto-scale (default) or Stabilize Only with a later reframe.
   Watch the auto-scale percentage; above ~110% softens the image noticeably.
5. "Detailed Analysis" for difficult shots (slower).

## Point-based Stabilize Motion (manual, precise)

Tracker panel - Stabilize Motion: track one point (position) or two (rotation/scale) on a static
background feature, apply to the layer's anchor point. Gives exact control and no warping; fill
edges with scaling or a background.

## Rendered/animated content

Rendered shots should not need stabilising. Common uses here: reference video shot handheld,
rotoscope plates, screen recordings of animatics on phones, live-action plates for mixed media.

## Gotchas

- Warp Stabilizer needs the layer's dimensions to match the comp (no scaling or precomp tricks
  before it); otherwise it asks you to precompose.
- Moving foreground objects can be read as camera motion; use "Show Track Points" and delete points
  on movers, then re-stabilise.
- Rolling shutter jello: enable Rolling Shutter Ripple options in Advanced or fix before stabilising.

## Verify

Toggle the effect on/off: background features hold steady (or move smoothly), no rubbery warping on
straight lines, scale increase acceptable for the delivery resolution.
