---
id: creative-arts.animation.motion-graphics.mocha-planar-tracking
name: mocha-planar-tracking
category: creative-arts
field: animation
product: motion-graphics
tags: [planar-tracking, motion-tracking, mocha-ae, mocha-pro, surface, corner-pin, screen-replacement, after-effects, boris-fx]
level: advanced
status: draft
description: "Planar-track surfaces with Mocha AE/Pro for screen replacements and signage: layer splines, surface alignment, exporting corner pin data back to After Effects."
sources:
  - https://borisfx.com/documentation/mocha/
  - https://helpx.adobe.com/after-effects/using/mocha-ae.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Planar tracking with Mocha

**Goal:** stick an image or video onto a flat surface that moves in perspective (phone screen, sign,
poster, tabletop) with no slipping. Planar trackers track a whole textured plane instead of points,
so they survive partial occlusion and motion blur far better.

## Procedure (Mocha AE in After Effects, Mocha Pro similar)

1. Apply Mocha AE to the footage layer (Effect - Boris FX Mocha - Mocha AE), click the Mocha logo.
2. Draw an **X-spline** around a textured planar area that moves as one plane (the screen bezel, not
   the content on the screen, which changes).
3. Track forward (and backward). Watch the spline follow.
4. Add occlusion layers above (fingers, hands) and set them to exclude: draw a spline on the
   occluder, track it, place it above the main layer in the layer list.
5. Turn on the **Surface** (S button); align its four corners to the actual screen corners on a
   frame where they are visible. Check other frames; adjust with Align Surface if needed.
6. Close Mocha, back in AE: in the effect's Tracking Data, **Create Track Data**, then Apply Export:
   Corner Pin (or Corner Pin with motion blur) to the replacement layer.

## Tips

- Track texture, not edges alone: a plane with text, scratches or patterns tracks best.
- For shots with lens distortion, undistort first (Mocha Pro lens module or AE lens tools), or
  pins will swim at frame edges.
- Rendered CG shots: export the screen's corner positions from the 3D app instead; tracking is for
  cases where data is not available.

## Gotchas

- Tracking the screen's own content (changing pixels) makes the track jump.
- Shear and perspective options: enable Perspective for strong angle changes, otherwise leave Shear
  only for stability.
- Corner pin data applies to the layer's original size; precompose the replacement at the exact
  aspect of the screen.

## Verify

Play through with the replacement at 100% and 200%: corners stay locked on the bezel through the
whole shot, including blurred frames and around occlusions.
