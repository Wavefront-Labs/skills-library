---
id: creative-arts.animation.blender.nla-strip-time-influence
name: nla-strip-time-influence
category: creative-arts
field: animation
product: blender
tags: [blender, nla, nla-strip-time, strip-repeat, strip-scale, reverse-strip, nla-animated-influence, animated-strip-time, sync-length]
level: practitioner
status: docs-checked
description: "Retime NLA strips in Blender: action frame range vs strip frames, Scale, Repeat, Reversed, Sync Length, and keyframing strip Influence and Strip Time for speed ramps and fades."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/nla/sidebar.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/editing/strip.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# nla-strip-time-influence

Goal: reuse one cycle many times, at different speeds, with fades, without editing the action.

## Strip panels (Sidebar > Strip)

- **Active Strip**: **Frame Start** moves the strip (duration constant); **Frame End** changes the strip and also the Action Clip Frame End, cropping or extending the action. To speed up or slow down, use Strip > Transform > Scale (S) or **Playback Scale**.
- **Action Clip**: **Frame Start/End** choose which part of the action is used (extending it lets F-curve extrapolation kick in). **Playback Scale**: below 1 plays faster, above 1 slower. **Repeat**: plays the action multiple times.
- **Reversed** (Playback): the strip plays backwards. **Cyclic Strip Time**: wraps Animated Strip Time back to the start if it exceeds the Action Clip Frame End.
- **Sync Length**: sets Frame Start/End to the action's first/last keyframe automatically when exiting Tweak Mode. **Now** does it immediately (same as Strip > Sync Action Length).
- Strip > Transform > Scale uses the Playhead as pivot; Clear Scale (Alt-S) resets it; Apply Scale (Ctrl-A) applies it to the action.

## Animated Influence

Tick **Animated Influence**, type a value, then insert a keyframe (context menu, or I while hovering). The curve shows in the Graph Editor. It is an alternative to (Auto) Blend In/Out.

## Animated Strip Time

Tick **Animated Strip Time** and keyframe **Strip Time**. Its value is a frame number inside the action, not inside the strip (action 1 to 50 in a strip at 101 to 150: set 1 to see the first key). With **Cyclic Strip Time**, animating it from 1 to 100 over a 1 to 50 action plays the keys twice at double speed. For simple repeats, use **Repeat**.

## Recipes

- Walk cycle across a shot: Repeat the cycle action; root motion via Cycles offset or a Follow Path.
- Slow-mo impact: key Strip Time so that scene frames advance more than action frames in that section.

## Gotchas

- Edit numeric fields rather than dragging if you need whole-frame strip ends.
- Bake (Strip > Bake Action) if downstream tools ignore NLA; it creates a key on every scene frame of the final motion.

## Verify

Scrubbing matches the intended speed; the Graph Editor shows the influence or strip-time curve.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), NLA Sidebar and Editing Strips: Active Strip and Action Clip fields, Playback Scale direction, Sync Length/Now, Animated Influence and Strip Time semantics, Bake Action. Removed as unconfirmed: strip length formula, fractional repeat, "Animated Strip Time ignores Scale/Repeat", numeric slow-mo example, sim-cache remark.
Method: documentation only; no commands were run.
