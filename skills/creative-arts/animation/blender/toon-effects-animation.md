---
id: creative-arts.animation.blender.toon-effects-animation
name: toon-effects-animation
category: creative-arts
field: animation
product: blender
tags: [blender, effects-animation, smears, impact-flash, smoke-puff, speed-lines, debris, fx-cards, boiling, cycling, on-twos, grease-pencil, shape-keys, cel, toon]
level: advanced
status: docs-checked
description: "2D-style FX animation in Blender: stepping on twos, smears, flashes, puffs, and boil via Displace and Grease Pencil Build/Noise."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/noise.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Toon effects animation (Blender)

Goal: the hand-drawn effects-animation vocabulary (smears, impact flashes, smoke puffs, debris, speed lines) in a 3D cel pipeline, so it reads as drawn elements in the shot rather than 3D simulation. The principles are shape, timing on twos, and the boil. This is the animation craft; the particle, smoke and fluid systems are separate skills.

## The three laws

1. **Shape over detail.** Design the silhouette at peak as a few bold, readable shapes, then work out how it grows into and out of it.
2. **Timing on twos, with holds.** Hand-drawn FX typically change drawing every second frame; the deliberate step is part of the look. Fast beats can drop to ones, slow drifts can go to threes. Effects snap to a peak shape and hold before dissipating.
3. **The boil.** A held drawn shape wobbles slightly from drawing to drawing; fake it so FX do not look frozen between key shapes.

## Stepping 3D motion onto twos

- **Stepped Interpolation F-Curve modifier:** select the FX object's F-Curve in the Graph Editor and add the modifier from Add F-Curve Modifier or the Sidebar's Add Modifier dropdown. It samples the curve every N frames and holds the value after each sample (choppy motion). *Step Size* is the number of frames to hold each step (2 for twos); *Offset* shifts the sample points.
- Key > Interpolation Mode (shortcut `T`) sets the interpolation of selected keyframes; a keyframe-level hold is an alternative to the modifier.
- Step per element rather than the whole scene, so FX, characters and camera can each have their own cadence.
- For Grease Pencil, draw a new keyframe on the chosen cadence.

## Classic elements (craft)

- **Smear:** a single elongated in-between bridging two extremes. In 3D, swap to a stretched smear object or a shape key for a frame or two, arced along the motion path, then snap back.
- **Impact flash:** a flat bright shape (a starburst or spike silhouette rather than a soft glow) that appears briefly at the contact point, peaks, then cuts instead of fading. The edit sells the hit: a brief full-frame flash and camera shake in comp help.
- **Smoke puff:** a few rounded lobes growing, rising and breaking into smaller shapes as it dissipates. Build a short shape-key or object-swap cycle and loop or offset it for a stream.
- **Speed lines:** thin streak cards or Grease Pencil strokes behind a fast object, present for a few frames, bold and few.
- **Debris and dust:** a few big readable chunks with eased, arced motion, stepped like the rest.
- **Flame:** a silhouette cycling through a few drawings; looping gives steady fire.

## Faking the boil

- **Displace modifier** driven by a texture whose mapping is animated slowly (for example from the frame number via a driver). Displace offsets vertices by `(texture value - Midlevel) x Strength` along a chosen Direction (axis, Normal, or per-channel RGB to XYZ), and a vertex group can limit it. Keep strength small; step the driver with the Stepped modifier so the wobble has drawn cadence.
- **Shape-key cycle:** a few boil shape keys with a looping stepped F-curve.
- **Grease Pencil Noise modifier:** adds varied values to stroke location, strength, thickness or UV rotation, with Noise Scale, Noise Offset and Seed. Its Mode *Steps* produces a new random value at defined steps (use for a jitter boil on a chosen cadence).

## Grease Pencil as a 2D FX layer

Grease Pencil strokes live in 3D space: parent a drawing plane to the camera for screen-space FX or place it in the scene for parallax. The **Build modifier** makes strokes appear or disappear over a frame range to animate lines being drawn or erased (Sequential, Concurrent and Additive modes; timing by speed, fixed length, or a manual percentage Factor from 0 to 1). Put FX on their own layer so they can be graded or glowed independently in comp.

## Keeping FX on-model

Use flat fills or flat emission to match the cast. Thin FX such as sparks and speed lines usually look better with the line drawn into the shape. Give FX their own render layer so comp can grade them separately.

## Checked

2026-11-09. Confirmed against the Graph Editor F-Curve Modifiers and Editing pages, Grease Pencil Build and Noise modifier pages and the Displace modifier page: Stepped Interpolation (Step Size, Offset, add menu), Interpolation Mode menu and shortcut, Displace formula and options, Noise modifier targets and Steps mode, Build modifier purpose, modes and Factor. The animation-craft passages (twos, smears, flashes, puffs) are professional practice, not documented in the manual. Removed: specific frame counts, lobe and point counts, 12 drawings per second, Constant interpolation option (not listed on the page), view-transform and outline-pipeline claims.
Method: documentation only; no commands were run.

## Verify

1. Scrubbing frame by frame shows new shapes on the chosen cadence, not a smooth per-frame update.
2. At the peak frame the effect is a few bold, readable silhouettes.
3. A held shape wobbles subtly.
4. Flashes and smears hit a peak and snap rather than fade.
5. FX are flat-filled, match the cast's line weight and sit on their own comp layer.
