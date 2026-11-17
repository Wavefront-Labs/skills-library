---
id: creative-arts.animation.blender.fcurve-stepped-generator
name: fcurve-stepped-generator
category: creative-arts
field: animation
product: blender
tags: [blender, fcurve-modifiers, stepped-modifier, stepped-interpolation, on-twos, generator-modifier, built-in-function, procedural-animation]
level: practitioner
status: docs-checked
description: "Use Blender's Stepped Interpolation F-modifier for on-twos looks (step size, offset, range) and Generator/Built-in Function modifiers for formula-driven motion."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/modifiers.html
  - https://docs.blender.org/api/current/bpy.types.FModifierStepped.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fcurve-stepped-generator

## Stepped Interpolation

Goal: spline-animated motion displayed on twos or threes (stop-motion or anime feel) while keeping smooth curves underneath.

- The modifier samples the curve every N frames and holds the value after each sample, lowering the curve's effective frame rate.
- **Step Size**: frames to hold each step (the API default is 2, that is, on twos). **Offset**: frames to offset the sample points. **Start Frame / End Frame**: limit where the effect applies.
- Add via Channel > Add F-Curve Modifier (Shift-Ctrl-M) > Stepped Interpolation on the active curve, or Sidebar > Modifiers; repeat per curve.
- Vary per shot section with Start/End Frame (for example ones in fast action, twos in holds).
- Stepped vs Constant interpolation: Constant holds the keys; Stepped samples the smooth curve every N frames.

## Generator

- **Mode**: *Expanded Polynomial* (y = A + Bx + Cx^2 ... , highest power set by **Order**) or *Factorized Polynomial* (y = (Ax + B)(Cx + D)). **Constant** holds the coefficients A, B, C...
- **Additive**: add the polynomial to the curve instead of replacing it. x is the frame, so with Additive off a first-order polynomial gives straight-line motion at constant speed (B = speed per frame) without keys.

## Built-in Function

- **Type**: Sine, Cosine, Tangent, Square Root, Natural Logarithm, Normalized Sine (sin(x)/x).
- **Amplitude** (Y scale), **Phase Multiplier** (X scale), **Phase Offset** (X offset), **Value Offset** (Y offset), **Additive**.
- For Sine the period in frames is 2 pi divided by Phase Multiplier (computed from y = A sin(m x + p)).

## Gotchas

- Generator and Built-in Function replace the keyed curve unless Additive is on, so keys look ignored.
- Modifiers evaluate top to bottom and can be reordered by dragging; Influence and Restrict Frame Range apply to each.
- To convert the result into keys, use Channel > Bake Channels with Bake Modifiers.

## Verify

The Graph Editor shows a staircase (Stepped) or the analytic curve; playback holds on the expected frames.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source) and API reference: Stepped fields and default step 2, Generator modes/Order/Constant/Additive, Built-in Function types and fields, modifier ordering, Bake Modifiers. Removed as unconfirmed: "Only Active" option, add-on suggestion, sound-curve scaling use (a polynomial in frame cannot scale a curve unless Additive), amplitude/multiplier examples, engine-export claim.
Method: documentation only; no commands were run.
