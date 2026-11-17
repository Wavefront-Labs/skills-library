---
id: computing-software.computer-graphics-engineering.rendering-techniques.froxel-volumetric-fog
name: froxel-volumetric-fog
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetric-rendering, participating-media, volumetric-fog, froxel, in-scattering, henyey-greenstein, light-shafts, temporal-reprojection]
level: advanced
status: docs-checked
description: "Render volumetric fog and light shafts with a camera-aligned froxel volume: density and lighting pass, ray-march accumulation, application, temporal jitter."
sources: ["https://bartwronski.com/wp-content/uploads/2014/08/bwronski_volumetric_fog_siggraph2014.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Froxel volumetric fog

**Goal:** fog that receives shadows (light shafts), local lights and height falloff, applied to
opaque and transparent geometry at a small fixed cost. The structure below follows Bart
Wronski's SIGGRAPH 2014 talk on Assassin's Creed 4 volumetric fog.

## 1. The volume
A camera-frustum-aligned 3D texture: the frustum maps to a cuboid with normalised device
coordinates across width and height, and an **exponential depth distribution** concentrating
slices near the camera (where precision matters most and aliasing shows). The talk used
160x90x64 or 160x90x128 depending on platform, giving a cost independent of screen resolution
(160x90x64 equals the texel count of a 720p surface, with lighting computed once per cell). The
range was artist-set between 50 and 128 m; longer range is possible with exponential
distribution or a cascaded approach. A world-aligned cuboid was tried first; it filters easily
over time but needs many samples to ray march, is slow and aliases.

Low resolution is enough because the volume stores low-frequency data per depth, the final
lookup is quadrilinear filtered, and every pixel uses its own native-resolution depth. The result
is soft and lacks high-frequency geometric detail, as multiple scattering does in reality.

## 2. Passes (compute)
1. **Shadow preparation**: downsample the cascaded shadow maps (four cascades in the talk) into
   an exponential shadow map target (R32F), which filters the shadowing probability and
   removes aliasing. ESMs are not practical for regular rendering but suit this.
2. **Density and lighting** per cell (combinable, or split): density from one octave of
   wind-animated Perlin noise (more octaves added little), plus vertical attenuation with an
   exponential distribution near the ground. Lighting accumulates the main light (with the ESM
   shadow), a constant ambient term and artist-flagged dynamic point lights intersecting the
   frustum. The talk stored lighting modulated by density in RGB and the scattering coefficient
   in alpha. Its phase function was art-driven (two colours, toward and away from the sun,
   otherwise isotropic); a physically based one such as Henyey-Greenstein can be used.
3. **Ray march**: a 2D compute thread group marches through the volume slices from the camera,
   accumulating in-scattered light and density (extinction, via Beer-Lambert) into a volume
   texture, giving per texel the light in-scattered from the camera to that point and the
   accumulated density.
4. **Apply** in forward or deferred shading: a bilinear 3D texture lookup and a fused
   multiply-add. Because whole view-ray data is stored, any number of transparent layers get
   correct fog.

Cost reported in the talk: about 1.1 ms total, 1.6 ms at double resolution, with density and
lighting about 0.43 ms and other passes under 0.2 ms each.

## 3. Optimisations and improvements named in the talk
- Early-out for volume parts behind rendered geometry, using a hierarchical Z buffer.
- Reuse the volume lighting for particles and other translucent objects.
- Past some distance, drop shadowing and lighting detail.
- Future work: physically based phase functions and SH-based ambient, temporal reprojection with
  per-frame sample jittering (reprojection is easier in 3D than 2D), and spatial jittering.
  Reprojection can still show ghosting on dynamic objects and with strongly view-dependent
  phase functions.

## Verify
- [ ] Sun shafts through gaps are visible and stable when the camera moves.
- [ ] No banding or stepping in dense fog.
- [ ] Transparent particles are fogged consistently with opaque geometry.

## Checked

Method: docs-checked 2026-11-09 against Wronski's SIGGRAPH 2014 slides (PDF converted to text; the volume layout, pass structure, cost and future-work sections read). Dropped the Frostbite article, RTR4 and PBR book sources (not read) and all claims from them: the analytic energy-conserving integration formula, 90-95 percent history blend, g range and the 100-200 m / 1 ms targets.
