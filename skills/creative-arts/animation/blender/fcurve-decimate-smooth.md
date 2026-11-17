---
id: creative-arts.animation.blender.fcurve-decimate-smooth
name: fcurve-decimate-smooth
category: creative-arts
field: animation
product: blender
tags: [blender, animation-cleanup, decimate-fcurves, decimate-keyframes, smooth-keys, sample-keyframes, butterworth, gaussian-smooth, mocap-cleanup]
level: practitioner
status: docs-checked
description: "Reduce and smooth dense keys in Blender's Graph Editor: Decimate by ratio or error, Gaussian, Butterworth and legacy Smooth, Bake Keyframes, for mocap cleanup."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fcurve-decimate-smooth

Goal: turn every-frame keys (mocap, simulations baked to keys, Bake Action) into editable, smooth curves.

## Decimate (Graph Editor > Key > Density)

- Menu items **Decimate (Ratio)** and **Decimate (Allowed Change)**; the operator's Mode is *Ratio* or *Error Margin*. It removes the keyframes that influence the curve's shape least.
- **Ratio**: *Remove* is the percentage of keyframes to delete.
- **Error Margin**: deletes as many keys as possible while the curve shape changes no more than **Max Error Margin**. Usually the better choice because it bounds the deviation.
- Works on the selected curves; do it per body part to keep detail on hands and face.

## Smooth (Key > Smooth)

- **Smooth (Gaussian)**: click the menu item, move the mouse to set strength, click to confirm. Options: Factor, Sigma (lower = sharper), Filter Width (wider looks at more keys).
- **Butterworth Smooth**: same modal use. Preserves the peaks of the animation, so it suits large amounts of data, but can introduce a ripple when values change rapidly. Options: Frequency Cutoff (lower = smoother; the useful maximum is half the sample rate, which is the scene frame rate times Samples per Frame), Filter order (higher = steeper cutoff), Samples per Frame (raise to 2 when keys are on subframes, for example a 60 fps file in a 30 fps scene), Blend, Blend In/Out.
- **Smooth (Legacy)** (Alt-O): strong smoothing; the first and last keys of the selection are kept.
- A Smooth (Gaussian) F-curve modifier does the same non-destructively; it must be first in the modifier stack.

## Bake Keyframes (Key > Density, Shift-Alt-O)

Creates a keyframe on every frame. For control over range, step and interpolation use Channel > Bake Channels (Frame Range, Frame Step, Remove Outside Range, Interpolation Type, Bake Modifiers, which bakes the modified curve and deletes the modifiers).

## Clean Keyframes (Key > Density)

Deletes keys equal to their neighbours; Threshold also removes nearly-equal keys. See `clean-channels`.

## Workflow (mocap)

1. Fix Euler flips first (Channel > Discontinuity (Euler) Filter; select all three rotation channels).
2. Smooth noisy channels only (fingers, hips) with Butterworth or Gaussian.
3. Decimate with Error Margin to make the curves editable.
4. Fix foot contacts by hand.

## Gotchas

- Smooth before decimating, otherwise noise survives as keys.
- Smoothing smears Euler flips; run the Discontinuity filter first.

## Verify

The key count drops with no visible change in motion; no jitter in hands or hips.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Decimate menu names and modes, Smooth menu names, Gaussian and Butterworth options and explanations, Smooth (Legacy) Alt-O, Bake Keyframes Shift-Alt-O (the skill previously called it Sample Keyframes, Shift-O), Bake Channels options, Clean Keyframes threshold, Discontinuity (Euler) Filter. Removed as unconfirmed: cutoff in Hz, error values, 80 percent figure, "better than Gaussian".
Method: documentation only; no commands were run.
