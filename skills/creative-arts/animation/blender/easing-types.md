---
id: creative-arts.animation.blender.easing-types
name: easing-types
category: creative-arts
field: animation
product: blender
tags: [blender, animation, easing-types, easing, elastic-interpolation, bounce-interpolation, interpolation-modes, motion-graphics]
level: practitioner
status: verified
description: "Use Blender's per-key interpolation and easing: Constant, Linear, Bezier, the Sine to Circular easings, Back/Bounce/Elastic with amplitude and period, and Ease In/Out/Auto."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# easing-types

Goal: fast, exact mograph motion (UI animations, logos, bounces) without hand-shaping handles.

## Interpolation (Graph Editor: Key > Interpolation Mode, T; select keys first)

Applies to the segment *from* the selected key to the next one.
- **Constant** (stepped), **Linear**, **Bézier** (the default; handle-driven).
- **Easing (by strength)**: Sinusoidal, Quadratic, Cubic, Quartic, Quintic, Exponential, Circular (the manual's order, not a strict strength order: for a 0 to 2 move over 24 frames the Ease In value at frame 6 was Sine 0.115, Quad 0.095, Circular 0.048, Cubic 0.021, Exponential 0.007, Quartic 0.004, Quintic 0.001 in Blender 4.5.14). Python `Keyframe.interpolation` ids: SINE, QUAD, CUBIC, QUART, QUINT, EXPO, CIRC, BACK, BOUNCE, ELASTIC.
- **Dynamic effects** (imitated physics): **Back** (overshoot; *Back* sets size and direction), **Bounce**, **Elastic** (*Amplitude* is the first overshoot, *Period* the time between oscillations).

## Easing direction (Key > Easing Type, Ctrl E, or N panel > F-Curve > Active Keyframe)

Only applies to the Easing and Dynamic Effects interpolations.
- **Automatic Easing**: Ease In for the Easing interpolations, Ease Out for the Dynamic Effects.
- **Ease In** (slow start, speeds up), **Ease Out** (fast start, slows down), **Ease In Out**. Python `Keyframe.easing`: AUTO, EASE_IN, EASE_OUT, EASE_IN_OUT, with `back`, `amplitude` and `period` fields. Measured: Automatic and Ease Out gave identical curves for Back, Bounce and Elastic, and Automatic gave the slow-start (Ease In) curve for the Easing family.

## Recipes (starting points from practice, not from the manual)

- **UI pop-in**: scale 0→1 over about 8 frames, Back, Ease Out; tune the Back amount for the overshoot.
- **Drop and bounce**: Z from 2→0 over about 20 frames, Bounce, Ease Out.
- **Spring settle on rotation**: Elastic, Ease Out; tune Amplitude and Period (a larger Period means more time between wobbles).

## Gotchas

- Dynamic easings (Back, Elastic) overshoot past key values by design; Bounce and Elastic decay over the segment.
- Check the exporter's documentation for how it handles these interpolation modes, and bake keys if the result differs (see `fbx-animation-export`).

## Verify

Graph Editor shows the characteristic curve shape between the two keys; the N panel Active Keyframe shows the interpolation and easing fields set.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), plus the interpolation enum in rna_curve.cc. Confirmed: Constant, Linear and Bézier (default) plus the seven Easing (by strength) names and Back, Bounce, Elastic with Amplitude and Period (editors/graph_editor/fcurves/properties.rst and rna_curve.cc); Easing options Automatic Easing, Ease In, Ease Out, Ease In Out and that they only apply to Easing and Dynamic Effects; Key > Interpolation Mode (T) and Key > Easing Type (Ctrl E) in fcurves/editing.rst. Wrong in the old text: the option is Ease In Out, not Ease In and Out. Removed the claims that easing preserves Bezier handles and that Auto Clamped neighbours change overshoot, and the numeric recipe values (kept as practice starting points).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: enum ids above, fcurve evaluation of every interpolation with Automatic/Ease Out; Back peaked at 2.159 on a move to 2.0 and Elastic at 2.012 (overshoot), Bounce stayed below 2.0. Error found: the 'least to most dramatic' ordering of the easing family did not hold (Circular and Exponential sit between Cubic and Quintic). Unrun (documentation only): T and Ctrl E shortcuts, the Active Keyframe panel, exporter behaviour, the recipes.

Method: manual text confirmed from documentation; curves run headless in Blender 4.5.14.
