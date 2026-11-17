---
id: creative-arts.animation.blender.cycles-clamping-fireflies
name: cycles-clamping-fireflies
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, clamping, fireflies, clamp-indirect, light-paths]
level: practitioner
status: docs-checked
description: "Kill Cycles fireflies at the source and with clamping: direct vs indirect clamp, energy loss trade-off, filter glossy, and finding the light path that causes them."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/cycles/optimizations/reducing_noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-clamping-fireflies

Goal: remove isolated over-bright pixels without dulling the image.

## Find the cause first

Fireflies come from light paths that are hard to find but carry a lot of light, for example a small light making a sharp highlight that is seen through a rough glossy surface (effectively a caustic). Use the Diffuse/Glossy/Transmission Indirect passes to see which carries them, then:

- Glossy paths: raise **Filter Glossy** (Light Paths > Caustics; the manual suggests 1.0 as a starting value) so such paths are blurred.
- Caustic paths: untick **Reflective / Refractive** caustics if the look allows it.
- Small bright emitters: use real lights, or adjust Emission Sampling in Material Properties > Settings (None, Auto, Front, Back, Front and Back).
- HDRI with a small sun: World > Settings > Sampling (Auto or Manual enables multiple importance sampling; the manual says to enable it for an image texture with small bright areas like the sun, at the cost of some firefly-like artifacts).

## Clamping (Render Properties > Light Paths > Clamping)

- **Direct Light** limits the intensity a sample from rays that have not yet bounced can contribute to a pixel. **Indirect Light** does the same for rays that have bounced. 0.0 disables clamping altogether.
- Lower values have a greater effect (dimmer samples) than higher values. Clamping reduces noise at the cost of accuracy, and other bright lights and reflections are dimmed as well.
- The manual advises clamping indirect bounces separately, since they cause more fireflies than direct ones and direct highlights stay untouched.
- Start with a high value and lower it until fireflies disappear at your final sample count, then stop.

## Gotchas

- Clamping is biased: image brightness changes with the value. Lock it before lighting approval.
- The denoiser does not remove fireflies. Fix the source first.
- EEVEE has its own clamp settings (see eevee-sampling-clamp).

## Verify

Compare a zoomed crop of the problem area before and after. No isolated hot pixels, and a midtone sample (Image Editor sample tool) should barely change.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Light Paths, Reducing Noise, World settings, Material settings). Confirmed: Direct/Indirect clamp semantics and 0.0 disable, Filter Glossy and Caustics toggles, Emission Sampling options, World Sampling behaviour. Removed unconfirmed: default clamp values, suggested clamp ladder, pass-to-cause mapping specifics.
Method: documentation only; no commands were run.
