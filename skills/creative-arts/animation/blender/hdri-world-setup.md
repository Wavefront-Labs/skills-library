---
id: creative-arts.animation.blender.hdri-world-setup
name: hdri-world-setup
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, hdri, hdri-world-setup, hdri-rotation, hdri-strength, environment-texture]
level: practitioner
status: docs-checked
description: "Light Blender scenes with an HDRI world: Environment Texture, Mapping rotation, Background strength, sun alignment, importance sampling map and colour space."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/world.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/environment.html
  - https://docs.blender.org/manual/en/latest/render/cycles/world_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/world_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hdri-world-setup

## Node setup (World > Surface)

The world surface accepts only the Background node (colour plus Strength). For image based lighting use the **Environment Texture** node rather than Image Texture for correct mapping; it supports Equirectangular (latitude/longitude) and Mirror Ball projections. Typical chain: Texture Coordinate -> Mapping (rotation to turn the HDRI) -> Environment Texture -> Background -> World Output. The Environment Texture **Color Space** list comes from the active OCIO config (see image-color-space).

## Strength and exposure

Use Background Strength for the world light level, or Film **Exposure** in Render Properties for overall brightness (separate from the Color Management exposure).

## Rotation

Rotate the Mapping node so the HDRI's sun or key aligns with the composition.

## Sampling

- Cycles (World > Settings): **Sampling** Auto or Manual enables Multiple Importance Sampling, which favours bright regions with an importance map and gives less noise for HDRIs with small bright areas such as the sun, at the cost of possible fireflies; None disables it. **Map Resolution** sets the importance map resolution: higher detects small features better but uses more memory and renders slightly slower.
- EEVEE (World > Settings): **Resolution** of the world light probe; **Sun > Threshold** records world contribution up to the threshold in the probe and converts the excess into a sun light (0 disables), with **Angle** and **Use Shadow** for the extracted sun.

## Gotchas

- A low-resolution HDRI as visible background looks blurry: the manual's Cycles world "tricks" use a Mix node with a Blend Factor of Is Camera Ray to separate the directly visible background from the lighting image (see hdri-backplate).
- A world Volume shader makes the world surface shader and sun lights have no effect.

## Verify

The HDRI sun direction matches the shadows; noise converges acceptably with Sampling set appropriately.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/lights/world (Environment Texture node for image based lighting, Equirectangular and Mirror Ball), render/cycles/world_settings (Sampling, Map Resolution, Multiple Importance), render/eevee/world_settings (Sun Threshold, Angle, Use Shadow, Resolution) and render/shader_nodes/textures/environment (Color Space follows the OCIO config). Removed unconfirmed Node Wrangler shortcut, 8-bit/JPG, polyhaven, strength and Mapping claims.
Method: documentation only; no commands were run.
