---
id: creative-arts.animation.blender.npr-rim-light
name: npr-rim-light
category: creative-arts
field: animation
product: blender
tags: [blender, npr-rim-light, stylized-rim, rim-light, fresnel, layer-weight, npr]
level: practitioner
status: docs-checked
description: "Add stylised rim light to toon materials: Layer Weight Facing or Fresnel into a stepped ramp, masking it to one side, and rim width and colour control."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/layer_weight.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# npr-rim-light

Goal: a crisp bright edge that separates characters from the background, as in anime and game toon shaders.

## Basic rim

```
Layer Weight (Facing or Fresnel) ─► Color Ramp (hard step) ─► rim mask
rim mask × rim colour ─► added onto the toon result
```
- The Layer Weight node has two angle-dependent outputs. The manual documents *Facing* as 1.0 when the surface faces the viewer and 0.0 at a grazing angle (purely orientation, independent of IOR), and *Fresnel* as 0.0 head-on and 1.0 at a grazing angle. Confirm in the viewport which end of the output is the silhouette, and invert the ramp if needed.
- *Blend* (default 0.5) controls the spread and sharpness: higher values sharpen the edge, lower values give a wider, more gradual blend. For *Fresnel*, Blend maps to IOR (0.5 = IOR 1.5).
- Rim width is mainly set by the ramp stop position, with Blend shifting the curve.
- The manual's own rim example is the *Facing* output into a Mix Shader Fac with an Emission shader in the first slot (Fac near 0 at the edges shows the first shader) and a Diffuse BSDF in the second; the *Fresnel* version swaps the slots.
- The optional *Normal* input lets a Bump node make the weight follow surface detail.

## Directional rim (only on one side)

Multiply the rim mask by a light-direction mask: dot(Normal, rim_light_vector) through a hard-step ramp, where `rim_light_vector` is driven from an empty behind the character (see `creative-arts.animation.blender.cel-light-direction`).

## Colour

Take the rim colour from the environment or a back light colour; add or screen it onto the toon result.

## Gotchas

- Flat or low-poly surfaces produce blocky rims; the rim follows the shading normal, so smooth shading and enough geometry matter.
- Inverted-hull outlines sit outside the rim; adjust the outline thickness so the rim stays visible.

## Verify

Turntable: the rim stays a consistent width on the silhouette, appears only on the intended side when masked, and does not appear on surfaces facing the camera.

## Checked

2026-11-09. Confirmed against the Blender manual Layer Weight node page (raw RST, read in full): Fresnel and Facing outputs and their documented ranges, Blend default and its IOR mapping, Normal input, the Emission / Mix Shader edge-glow example. Removed: numeric Blend and ramp-stop ranges, the EEVEE Shader to RGB light-linking alternative, the bloom claim and the Filmic/AgX desaturation claim (not on the page). The page's Facing polarity is stated as documented and flagged for a viewport check.
Method: documentation only; no commands were run.
