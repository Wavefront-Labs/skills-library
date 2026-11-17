---
id: creative-arts.animation.motion-graphics.ae-roving-keyframes
name: ae-roving-keyframes
category: creative-arts
field: animation
product: motion-graphics
tags: [roving-keyframes, keyframe-interpolation, after-effects, rove-across-time, constant-speed, motion-path, time-reverse-keyframes]
level: practitioner
status: draft
description: "Use roving keyframes in After Effects to get constant speed along multi-point motion paths, and when to lock them back; time-stretching and reversing key groups."
sources:
  - https://helpx.adobe.com/after-effects/using/keyframe-interpolation.html
  - https://helpx.adobe.com/after-effects/using/editing-moving-copying-keyframes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Roving keyframes

**Goal:** an object travels through several path points at even speed (a camera glide, a line drawing
across a map) without hand-retiming every middle key.

## How roving works

A roving keyframe is tied to a position on the path but not to a time: AE moves it in time so the
speed between the first and last (non-roving) keyframes is smooth. Applies to spatial properties
(Position, Anchor Point, effect points).

## Procedure

1. Set Position keyframes for the route; set first and last keys at the desired start/end times.
2. Select the middle keys - right-click - **Rove Across Time** (or Animation - Keyframe
   Interpolation - Roving: Rove Across Time). The keys become small dots and redistribute.
3. Ease the first and last keys (F9) if the motion should start and stop gently; middle keys follow
   the overall speed curve.
4. To tweak one middle key's timing again, uncheck rove on it (it becomes locked in time).

## Related keyframe-group operations

- **Time-stretch a group**: select keys, Alt-drag the first or last key to scale timing
  proportionally.
- **Time-Reverse Keyframes**: select keys, Animation - Keyframe Assistant - Time-Reverse Keyframes
  (an exit that mirrors the entrance).
- **Sequence Layers** (Keyframe Assistant) offsets layers in time for cascades.

## Gotchas

- First and last keys cannot rove.
- Changing the path shape (moving handles) re-flows roving key times; check landmarks still hit
  their story beat.
- Roving does not apply to non-spatial properties (opacity, scale) that should sync with the path;
  link those with expressions or by eye after roving settles.

## Verify

Motion path dots are evenly spaced between start and end eases; the speed graph is a smooth single
hump with no dips at middle keys.
