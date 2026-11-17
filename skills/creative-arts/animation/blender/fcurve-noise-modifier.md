---
id: creative-arts.animation.blender.fcurve-noise-modifier
name: fcurve-noise-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, fcurve-modifiers, noise-modifier, noise-phase-offset, noise-strength, noise-phase, fmodifier-frame-range, modifier-influence, restrict-frame-range, camera-shake]
level: practitioner
status: docs-checked
description: "Add procedural jitter with Blender's Noise F-curve modifier (scale, strength, phase, offset, depth, blend type) and limit it with Restrict Frame Range blend in/out and Influence."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/modifiers.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fcurve-noise-modifier

Goal: camera shake, flicker, idle jitter: procedural, non-destructive and timed to the shot.

## Noise settings

- **Blend Type**: *Replace* (adds noise in the range -0.5 to 0.5), *Add* (adds noise 0 to 1), *Subtract* (subtracts noise 0 to 1), *Multiply* (multiplies by noise 0 to 1).
- **Scale**: horizontal scale of the noise; higher values give less dense oscillation.
- **Strength**: vertical scale, in the channel's units (radians for rotation, so a Strength of 1 on rotation is a large spin).
- **Offset**: shifts the noise in time. **Phase**: changes the random seed; use a different Phase per axis so X/Y/Z do not move in sync.
- **Depth**: how detailed the noise is. **Lacunarity** (gap between successive frequencies) and **Roughness** (high-frequency detail) only have an effect when Depth is greater than 0.

## Common options (all F-curve modifiers)

- **Restrict Frame Range**: **Start/End** frames and **Blend In/Out** frames, the number of frames it takes the effect to fade in or out (a shake that decays).
- **Influence**: blends between the original and the modified curve.
- Mute (header checkbox) disables a modifier; the cross deletes it; drag the dots to reorder (evaluated top to bottom).

## Camera shake recipe

Parent the camera to an Empty named `shake`. On the Empty's rotation channels add Noise (Blend Type Add), a different Phase on each axis, a small Strength, and a Restrict Frame Range around the impact with a Blend Out. Keep the main camera move clean on the camera itself.

## Gotchas

- Strength is in radians for rotation channels.
- Add the modifier with Channel > Add F-Curve Modifier (Shift-Ctrl-M) to the active curve, or in Sidebar > Modifiers.
- To turn the modified curve into keys, use Channel > Bake Channels with **Bake Modifiers** enabled (the modifiers are then deleted).
- A Cycles modifier must be first in the stack, so any Noise modifier sits below it.

## Verify

The Graph Editor shows the modified curve; with Restrict Frame Range on, the curve is clean outside the range.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Noise blend type ranges, Scale/Strength/Offset/Phase/Depth/Lacunarity/Roughness semantics, Restrict Frame Range, Influence, modifier order, Shift-Ctrl-M, Bake Channels with Bake Modifiers. Removed as unconfirmed: specific Scale and Strength values, keyframing Influence, the "Noise before Cycles" claim (Cycles has to be first), engine-export claim.
Method: documentation only; no commands were run.
