---
id: creative-arts.animation.blender.bake-sound-fcurve
name: bake-sound-fcurve
category: creative-arts
field: animation
product: blender
tags: [blender, animation, bake-sound, sound-to-fcurve, audio-reactive, music-visualizer, graph-editor]
level: practitioner
status: docs-checked
description: "Drive animation from audio with Blender's Channel > Sound to Samples: frequency band, attack/release, threshold, accumulate, additive, square, then reuse via drivers."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bake-sound-fcurve

Goal: audio-reactive motion: speaker cones, equalizer bars, lights pulsing to a beat.

## Steps

1. Insert a key on the property you want to drive (for example Scale Z of a bar, or a custom property such as `beat` on an Empty, which is easier to reuse).
2. Graph Editor: select that F-curve, **Channel > Sound to Samples**.
3. Choose the audio file and options:
   - **Lowest Frequency**: cutoff of a high-pass filter applied to the audio. **Highest Frequency**: cutoff of a low-pass filter. Together they select the band to analyse.
   - **Attack Time** and **Release Time**: how fast the hull curve can rise and fall; the lower the value, the steeper it can go.
   - **Threshold**: minimum amplitude needed to influence the hull curve.
   - **Accumulate**: only positive differences of the hull curve are summed. **Additive**: the amplitudes are summed (with Accumulate, positive and negative differences both accumulate).
   - **Square**: square-wave output (negative values give -1, positive give 1); **Square Threshold**: values below it give 0.
4. The result is a sampled curve. Use **Samples to Keys** if you need to edit it (it creates a key on every frame), or rescale through a driver expression such as `var*5`.

## Reuse pattern

Bake each band into its own custom property on a control Empty (`kick`, `snare`, `hats`), then drive many objects from those properties with drivers; re-baking updates everything.

## Related curve tools (Channel menu)

- **Keys to Samples** (Alt-C): destructive; switches the curve to a sampled value at each full frame to shrink large datasets; interpolates linearly between samples.
- **Samples to Keys**: back to editable keyframes (one per frame).

## Gotchas

- The baked curve does not play the sound; add the audio in the Video Sequencer to hear it, aligned to the same start frame.
- Bake only the bands you use; sampled curves on many properties add up.

## Verify

Play with audio and check that peaks line up with the beats.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), Graph Editor Channel editing page: Sound to Samples location and every option definition, Samples to Keys, Keys to Samples. Removed as unconfirmed: example frequency bands, typical attack/release values, "Playback Sync" instruction, the older Key > Bake Sound menu name, file-size remark.
Method: documentation only; no commands were run.
