---
id: creative-arts.animation.blender.cycles-light-bounces
name: cycles-light-bounces
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, light-bounces, max-bounces, transparent-bounces, light-paths]
level: practitioner
status: docs-checked
description: "Tune Cycles Light Paths max bounces (total, diffuse, glossy, transmission, volume, transparent) and min bounces, and compare against a high-bounce reference."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-light-bounces

Goal: give each ray type just enough bounces. Too few loses light, too many costs time.

## Max Bounces (Render Properties > Light Paths > Max Bounces)

- **Total**: maximum number of light bounces. For best quality set it to the maximum; lower values render faster. 0 bounces gives direct lighting only.
- **Diffuse**, **Glossy**, **Transmission**, **Volume**: maximum bounces of that type.
- **Transparent**: maximum transparency bounces, controlled separately from the others. Probabilistic termination can help with many layers of transparency.

Light paths are terminated probabilistically when the minimum number of bounces is lower than the maximum: paths longer than the minimum are randomly stopped when they are expected to contribute less. The image still converges to the same result, faster but possibly noisier.

## Min bounces (Sampling > Advanced)

- **Min Light Bounces**: bounces after which Russian Roulette terminates low-contribution paths. Higher gives less noise but can raise render time considerably. For a low maximum, the manual strongly recommends setting the minimum to the same value.
- **Min Transparent Bounces**: minimum transparent passthroughs. Higher reduces noise in the first bounces but can be less efficient for hair and volumes.

## Transparency

The Transparent BSDF is special: rays pass straight through without changing direction or type, but each step still runs the shader and traces a ray, so many transparent layers cost time. Other transmission BSDFs count as opaque in the alpha pass.

## Workflow

1. Render a reference crop with high values for every type.
2. Lower one type at a time on the real scene and compare the crop.
3. Ship the cheapest settings whose difference from the reference is below your noise level.
4. A per-light **Max Bounces** (light settings) is limited by these scene-wide settings.

Fast GI (see cycles-fast-gi) can stand in for later diffuse bounces.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Light Paths, Sampling). Confirmed: each Max Bounces field and its meaning, 0 = direct only, transparent control, min bounce semantics, Fast GI link. Removed unconfirmed: default values, per-scene-type table, symptom diagnoses, speed percentages, the preset menu names.
Method: documentation only; no commands were run.
