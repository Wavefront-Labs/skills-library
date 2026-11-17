---
id: creative-arts.visual-art.procreate.animation-assist-onion-skins-and-timing
name: animation-assist-onion-skins-and-timing
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, animation-assist, procreate-animation, onion-skin, frame-timing, frames-per-second, hold-duration, frame-by-frame, timeline, ping-pong-loop]
level: intro
status: draft
description: "Animate frame by frame in Procreate Animation Assist: turning it on, frame rate, onion skin frames and opacity, hold duration per frame, adding and duplicating frames, and timing a loop."
sources: ["https://procreate.com/handbook/procreate/animation/animation-settings/", "https://procreate.com/handbook"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Animation Assist: onion skins and timing

**Goal:** short frame-by-frame animations in Procreate with controlled timing
(Procreate Handbook, Animation Assist and Settings).

## Turn it on
Actions > Canvas > **Animation Assist**. A timeline appears at the bottom;
each top-level **layer or group = one frame**.

## Settings (Settings button on the timeline)
- **Playback**: Loop, Ping-Pong, One Shot.
- **Frames per second**: 1-60. Hand-drawn animation commonly uses 12 fps ("on twos"
  of 24) for a natural look; 24 for smoother motion.
- **Onion skin frames**: how many neighbouring frames are shown (up to about 12).
- **Onion skin opacity**: strength of ghosted frames.
- **Blend primary frame** and **Colour secondary frames** (previous frames tinted
  one colour, next frames another) to tell past and future apart.

## Frames
- **Add frame** button adds a new frame after the current one.
- Tap a frame thumbnail to select; tap again for **Hold duration** (repeat the frame
  for N frames, without redrawing), **Duplicate**, **Delete**.
- Groups as frames let you keep line and colour on separate layers in one frame.

## Timing workflow
1. Draw **key poses** first as frames; set rough holds.
2. Play back; adjust holds to get the timing right before drawing in-betweens.
3. Add in-betweens using onion skins (2-3 frames visible).
4. For a loop, make the last frame lead naturally into the first; check in Loop playback.

## Gotchas
- Layers accidentally added at top level become extra frames: group helper layers.
- Large canvases plus many frames hit layer limits; keep canvas small for animation.

## Verify
- [ ] Fps and playback mode set intentionally.
- [ ] Timing tuned with holds before in-betweening.
- [ ] Loop plays without a jump.
