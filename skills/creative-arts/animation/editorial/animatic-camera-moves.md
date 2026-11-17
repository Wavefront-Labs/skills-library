---
id: creative-arts.animation.editorial.animatic-camera-moves
name: animatic-camera-moves
category: creative-arts
field: animation
product: editorial
tags: [animatic-camera-moves, animatic, story-reel, pans, trucks, camera-moves, keyframes, oversized-boards, layout-handoff]
level: practitioner
status: draft
description: "Fake pans, trucks and shakes on storyboard panels in the animatic with keyframed position/scale, and hand layout a camera move it can reproduce exactly."
sources:
  - https://helpx.adobe.com/premiere-pro/using/animating-motion-program-monitor.html
  - https://docs.toonboom.com/help/storyboard-pro-22/storyboard/camera/about-camera.html
  - https://www.routledge.com/Producing-Animation/Winder-Dowlatabadi-Miller-Zarneke/p/book/9781138479937
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera moves in the animatic

**Goal:** the animatic shows the intended camera (pan, truck in, shake) at the right speed, and layout can rebuild
it from numbers rather than guesswork.

## Draw for the move

- Boards for a pan are drawn **oversized** (e.g. 1.5x-3x frame width) with the start and end frames marked as
  rectangles on the panel; a truck-in is drawn at the widest field with the end field marked.
- Ask story for panels at a known pixel scale: if the show raster is 1920x1080, a 2-field pan board is 3840 px wide.

## Keyframing in the NLE

- **Premiere:** Effect Controls > Motion > Position and Scale keyframes. Set the start frame, then the end frame;
  right-click the keyframes > *Ease In/Ease Out* for camera-like starts and stops, or *Linear* for a constant
  dolly. Storyboard Pro or Harmony can export the move instead (Storyboard Pro has a camera per panel).
- **Resolve:** Inspector > Transform (Zoom, Position) with keyframes; Dynamic Zoom for a quick Ken Burns move.
- **Shake:** use a tiny Position wiggle of 2-6 px for 4-8 frames (Premiere has no wiggle; key by hand or use an
  After Effects comp; see `creative-arts.animation.scripting.ae-wiggle-expression`).

## Handing the move to layout

Write the move as data, per shot: start field (centre x/y, width), end field, start/end frame, easing. Example:
`sh0040: pan L->R, field 12F -> 12F, centre x 960 -> 2880, frames 1-72, ease in 8 / ease out 12`.
Layout matches it in the DCC camera; the animatic's timing then survives into production.

## Gotchas

- Scaling a board above 100% of its pixel size softens it; truck-ins need boards drawn at the closest field's
  resolution.
- Pans that are too fast strobe: the classic guide is no more than about half the screen width per second at 24 fps
  for a smooth read; faster pans need motion blur or become whip pans with a cut.
- Speed must allow the audience to read what the camera reveals; time it against the scratch VO.

## Verify

Layout's first pass of the shot, laid over the animatic in the cut, shows the camera arriving on the same frame with
the same framing. Related: `creative-arts.animation.editing.animatic-assembly`.
