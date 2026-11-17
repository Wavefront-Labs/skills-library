---
id: creative-arts.animation.blender.grease-pencil-modifiers-fx
name: grease-pencil-modifiers-fx
category: creative-arts
field: animation
product: blender
tags: [blender, gp-modifiers, grease-pencil-modifiers, gp-effects, gp-build-modifier, grease-pencil, gpencil, build, noise, shader-effects, glow, blur, pixelate, rim]
level: advanced
status: docs-checked
description: "Grease Pencil modifiers and visual effects in Blender: the Build (write-on) and Noise (line boil) modifiers in detail, modifier categories and the FX list."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/index.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/noise.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# grease-pencil-modifiers-fx

Goal: get procedural motion, variation and post effects on 2D strokes without redrawing frames.

Grease Pencil modifiers are grouped into four categories: **Generate**, **Deform**, **Color** and **Edit**. Each modifier has *Influence* filters (see the manual's Influence Filters section) to restrict it. Visual Effects are a separate list of effects.

## Build modifier (Generate): write-on and erase

Makes strokes appear or disappear over a frame range, to animate lines being drawn or erased. (For other object types the general Build modifier applies.)

- **Mode**: *Sequential* (strokes appear/disappear one after the other, one at a time), *Concurrent* (several strokes at a time), *Additive* (builds only strokes that are new compared to the last keyframe, assuming Additive Drawing was used so shared strokes are identical).
- **Transition** (Sequential and Concurrent): *Grow* (shows points in stroke order, as if being drawn), *Shrink* (hides points from the end of each stroke back to the start, as if erased), *Vanish* (hides points in the order they occur, ink fading after drawing).
- **Timing**: *Natural Drawing Speed* (uses the recorded stylus speed; Sequential and Additive only; *Speed Factor* multiplies it, *Maximum Gap* is the longest gap between strokes in seconds), *Number of Frames* (*Frames* maximum, unless another keyframe occurs first; *Delay* frames after each keyframe before the modifier acts), *Percentage Factor* (*Factor* 0 to 1 sets how much is visible; animate it), *Time Alignment* (Concurrent only: *Align Start* or *Align End*).
- **Object**: use distance to an object to define the order strokes appear.
- **Custom Range**: only modify strokes between the Start and End frames.
- **Fade**: *Factor* (how much the stroke fades in/out), *Thickness* and *Opacity* (how much the fading applies to each), *Weight Output* (assigns a weight to points that have started or finished the fade).

## Noise modifier (Deform): line boil

Adds varied values to point location, strength (opacity), thickness or UV rotation, making the line unstable and noisy.
- **Position / Strength / Thickness / UV**: the strength of the noise on each property.
- **Noise Scale** (frequency), **Noise Offset** (moves the noise along the strokes), **Seed**.
- **Randomize**: when enabled the noise uses a random value over time. *Mode* *Steps* picks a new random value every *Step* frames; *Keyframes* picks a new value only on keyframes. A step above 1 gives line boil "on twos" or threes rather than every frame.

## Visual Effects

The effect types are Blur, Colorize, Flip, Glow, Pixelate, Rim, Shadow, Swirl and Wave Distortion. Check each effect's manual page for its settings in your Blender version.

## Verify

- Scrubbing shows Build revealing strokes over the set range.
- Noise with Randomize Mode Steps and Step 3 changes the line only every third frame.

## Checked

2026-11-09. Confirmed against the Blender manual pages for Grease Pencil Modifiers (category list), the Build modifier, the Noise modifier and the Visual Effects index (raw RST). Removed unconfirmed claims: the rest of the modifier catalogue and its option lists, recommended numeric noise values, stack-order rules, Apply behaviour, FX settings and render engine restrictions, and version notes on Grease Pencil v3.
Method: documentation only; no commands were run.
