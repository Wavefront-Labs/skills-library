---
id: creative-arts.animation.blender.cycles-seed-pattern
name: cycles-seed-pattern
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, seed-animation, animated-seed, sampling-pattern, scrambling-distance]
level: practitioner
status: docs-checked
description: "Control Cycles noise across frames: seed, Use Animated Seed, sampling Pattern (Automatic, Classic, Blue-Noise), scrambling distance and layer samples."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-seed-pattern

Goal: decide whether residual noise stays still or moves from frame to frame, and pick the sampling pattern.

## Render Properties > Sampling > Advanced

- **Seed**: seed value for the integrator to get different noise patterns. **Use Animated Seed** (clock icon; Python `scene.cycles.use_animated_seed`) changes the seed for each frame. The manual recommends enabling it for animation because a varying noise pattern is less noticeable.
- **Pattern**:
  - *Automatic*: uses Blue-Noise, with a tweak for viewport rendering to get better quality in the first sample (useful while the render keeps restarting during interactive changes).
  - *Classic*: pre-computed tables of Owen-scrambled Sobol.
  - *Blue-Noise*: optimises the frequency distribution; with the full number of samples the output typically looks smoother than Classic without actually reducing overall noise.
- **Scrambling Distance**: reduces randomness between pixels to try to improve GPU performance, at the cost of potential artifacts. Not compatible with the Blue-Noise pattern. Sub-options: *Automatic* (adapts to sample count), *Viewport* (faster but may cause flickering), *Multiplier* (values below one reduce the distance, which may help GPU speed but makes artifacts more visible).
- **Min Light Bounces / Min Transparent Bounces** (see cycles-light-bounces).
- **Layer Samples**: how view-layer sample overrides are used: Use, Bounded (overrides only up to the scene-level count), Ignore.

## Gotchas

- Rendering the same frame twice with the same seed gives the same noise. To combine two renders for lower noise, change the seed between them.
- Keep the Pattern the same across a whole sequence so the grain character matches between shots.
- Sample Subset (Offset/Length) renders part of the samples so work can be split across machines; set (Max) Samples to the full total on every machine, disable Denoise, and combine the EXRs with `bpy.ops.cycles.merge_images`, as the manual describes.

## Verify

Render three consecutive frames of a static camera with Use Animated Seed off, then on. The noise should stay locked with it off and change with it on.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual, Cycles Sampling (Advanced). Wrong claim fixed: the Pattern options in 5.2 are Automatic, Classic and Blue-Noise (not Tabulated Sobol). Confirmed: Seed and Use Animated Seed, Scrambling Distance options and Blue-Noise incompatibility, Layer Samples, Sample Subset. Removed unconfirmed: render-farm consistency claim, dirty-lens description, "leave off for finals" advice.
Method: documentation only; no commands were run.
