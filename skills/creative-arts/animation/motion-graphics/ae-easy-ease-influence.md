---
id: creative-arts.animation.motion-graphics.ae-easy-ease-influence
name: ae-easy-ease-influence
category: creative-arts
field: animation
product: motion-graphics
tags: [easy-ease, keyframe-interpolation, after-effects, keyframe-velocity, influence, temporal-interpolation, hold-keyframes, easing-presets, motion-design]
level: practitioner
status: draft
description: "Set temporal easing in After Effects precisely: Easy Ease variants, Keyframe Velocity influence values, hold keyframes, and consistent house easing curves."
sources:
  - https://helpx.adobe.com/after-effects/using/keyframe-interpolation.html
  - https://helpx.adobe.com/after-effects/using/speed.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Easy ease and influence

**Goal:** consistent, repeatable easing across a show's graphics package, set by numbers rather than
by eye on each layer.

## The tools

| Command | Shortcut | Effect |
|---|---|---|
| Easy Ease | F9 | 33.33% influence in and out, zero speed at the key |
| Easy Ease In | Shift+F9 | eases arriving at the key |
| Easy Ease Out | Ctrl/Cmd+Shift+F9 | eases leaving the key |
| Toggle Hold Keyframe | Ctrl/Cmd+Alt+H | value holds until the next key (stepped) |
| Keyframe Velocity dialog | Ctrl/Cmd+Shift+K | type speed and influence for in/out |

**Influence** (0.1-100%) is how far the handle reaches toward the neighbouring keyframe in time;
higher means a longer, gentler acceleration/deceleration.

## House curves (write them down)

Define three or four named eases for the show and use them everywhere:
- **Snap in**: out 10%, in 80% (fast entry, long settle) for titles and UI.
- **Gentle**: 50% / 50% for background drift.
- **Anticipate-out**: use an extra key with small reverse move, then out 70%.
Apply via the Keyframe Velocity dialog, a script, or a preset/extension (e.g. Flow, Ease and Wizz)
so values are identical across artists.

## Hold keyframes for limited animation

Hold keyframes give stepped motion: "on twos" style graphics or stop-motion feel. Combine with
`posterizeTime(12)` expression on a property for a global step rate.

## Gotchas

- F9 on combined Position sets temporal easing, but spatial interpolation (path shape) is separate
  (`creative-arts.animation.motion-graphics.ae-motion-paths`).
- Easing on both sides of a middle keyframe with Easy Ease makes the layer stop at that key; for
  continuous motion through a key, use auto bezier or continuous bezier instead.
- Influence values do not survive copying between layers with different distances in the same way
  speed does; check visually.

## Verify

Select a key, open Keyframe Velocity: values match the house curve. Frame-step through a transition
to confirm no unintended stop at intermediate keys.
