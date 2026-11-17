---
id: creative-arts.animation.blender.volumetrics-atmospherics
name: volumetrics-atmospherics
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, volumetrics, fog, god-rays, light-shafts, atmosphere, principled-volume, anisotropy, mist-pass, depth, world-volume, fog-cards, cel, stylized, render-cost]
level: advanced
status: docs-checked
description: "Fog and god-rays in EEVEE: volumes vs mist-pass depth fog vs flat cards, Principled Volume inputs, Volume Scatter, volume cost."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/world_settings.html
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/volumes.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_settings.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_principled.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# volumetrics-atmospherics

Goal: atmospheric depth (morning fog, god-rays, dusty shafts) in EEVEE without washing out a flat stylised picture or exploding render time. Core decision: **true volume, mist-pass fog, or a flat card?** Decide per shot, cheapest first.

| Tool | Cost | Parallax/3D | Use when |
|---|---|---|---|
| Volume objects (Principled Volume) | High | Yes | Light shafts with moving occluders or lights; camera passing through fog |
| Mist pass depth fog (compositor) | Low | Depth only | General aerial perspective |
| Flat fog planes or cards | Low | Layered | Ground fog, drifting wisps, drawn shaft shapes |

## Mist-pass depth atmosphere

1. Enable the Mist pass on the View Layer first; the World > Mist Pass settings are not available until then.
2. World > Mist Pass: **Start** is the distance from the camera where mist starts fading in; **Depth** is the distance from Start over which it fades in, and objects beyond Start + Depth are completely hidden by mist. **Falloff** is Quadratic (smoothest transition), Linear, or Inverse Quadratic (steepest start, approaches 1.0 fastest). The pass is a depth map from 0.0 to 1.0.
3. In the compositor, run the Mist pass through a ColorRamp (a constant interpolation gives banded steps) and mix a fog colour over the image. The ramp is the style control.
4. Keep characters clear: set Start beyond the acting plane, or matte them out (for example with Cryptomatte) before the mix.

## True volumes

- A Principled Volume can go in a World shader or in a material on a volume object. A scaled domain cube limits cost to where fog exists (world volumes fill the whole view frustum).
- Principled Volume inputs: Color, Density, Anisotropy (backward or forward scattering direction), Absorption Color (volume shadow tint), Emission Strength and Color, Blackbody Intensity and Temperature for fire. Keep Emission at zero for plain atmosphere. The Volume output goes to the Volume input of the Material or World Output node.
- Light shafts need occlusion: keep shadow casting on for the light and blocking geometry. The light's **Volume Scatter** is a volume light intensity multiplier; lower it on lights that should not contribute to shafts.
- Volumetric Shadows (Render > Sampling > Shadows) approximate light absorption by surrounding volumes and are described as very computationally expensive with limitations.
- **Render > Volumes:** Resolution and Steps tune the 3D textures, which use a lot of video memory; Steps are distributed along view depth; Distribution blends linear and exponential (higher puts more samples near the camera); Max Depth is the accurate-intersection surface count and creates artifacts when exceeded. Custom Range (Start/End) restricts volume computation along camera depth, useful with world volume shaders or many volume objects.
- EEVEE evaluates all volume objects inside the view frustum, so shrink domains to the fogged region and avoid overlapping domains.

## Flat fog cards

Cards (planes with an alpha mask) are the stylised alternative: art-directable, no volume cost, easy to layer for parallax. Exclude them from shadow casting and from any outline pass your pipeline uses.

## Exposure discipline

Fog adds light. After adding any, check in the compositor that the subject's fill tone has not shifted, and bring contrast back in comp rather than stacking more light. Shafts read best against a dark surround.

## Checked

2026-11-09. Confirmed against the EEVEE World (Mist Pass), Volumes, Light and Principled Volume manual pages: the mist settings, falloff names, Principled Volume inputs, Volume Scatter multiplier, volume texture settings and Custom Range, volume-frustum evaluation. Removed (not stated by the pages): numeric limits (5% fill shift, fog value 0.7, wisp timings), world-volume advice phrased as "almost always wrong", gobo planes, froxel pricing, flicker-fix ordering, Standard view transform rules and show-specific conventions.
Method: documentation only; no commands were run.

## Verify

- [ ] Every atmosphere effect is justified; true volumes only where needed.
- [ ] Raw mist pass shows characters in front of Start.
- [ ] Subject fill tone unchanged by fog when checked in comp.
- [ ] Only lights that make shafts have Volume Scatter raised.
- [ ] Atmosphere render cost is a small part of the frame; no flicker in a short test.
