---
id: computing-software.computer-graphics-engineering.rendering-techniques.subsurface-scattering
name: subsurface-scattering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, subsurface-scattering, sss, skin-rendering, separable-sss, burley-diffusion, pre-integrated-skin]
level: sme
status: draft
description: "Render real-time subsurface scattering for skin and wax: screen-space separable/Burley diffusion, pre-integrated skin, thin-object transmission, and tuning."
sources: ["https://www.iryoku.com/separable-sss/", "https://graphics.pixar.com/library/ApproxBSSRDF/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subsurface scattering (real time)

## 1. Pick the technique
| Need | Technique |
|---|---|
| Hero skin, deferred renderer | Screen-space diffusion blur of diffuse lighting (Jimenez separable SSS, or Burley normalized diffusion as in UE/Unity HDRP) |
| Forward/mobile, cheap | Pre-integrated skin: 2D LUT indexed by `N.L` and curvature |
| Ears, leaves, thin cloth | Transmission term from shadow-map thickness or a baked thickness map |
| Offline reference | Path-traced random-walk SSS |

## 2. Screen-space diffusion
- Render diffuse and specular to separate targets (or flag SSS pixels in stencil). Only diffuse is blurred;
  specular is surface reflection.
- Kernel world-space radius = the material's scattering distance (per channel; red scatters farthest in
  skin), projected to pixels with depth: `radiusPx = sssWidth * projScale / linearDepth`.
- Depth-aware weights: reject samples whose depth differs strongly (stops bleeding onto background).
- Burley profile: `R(r) = A*s*(exp(-s*r) + exp(-s*r/3)) / (8*pi*r)` with `s` from the albedo fit; importance
  sample radius from its CDF rather than a fixed Gaussian.
- Separable (two 1D passes) is an approximation; artefacts appear at silhouettes. Stencil-limit to SSS pixels.

## 3. Pre-integrated skin
Precompute `LUT(N.L, 1/r)` by integrating the diffusion profile over a ring of curvature `1/r`. Curvature from
`length(fwidth(N)) / length(fwidth(P))` or bake it per vertex. Sample a lower normal-map mip for the red
channel's diffuse to soften pores.

## 4. Transmission
`T = profile(thickness) * saturate(-N.L + wrap)`, thickness = light-space shadow depth minus receiver depth.
Add a thickness map for thin parts where the shadow map is too coarse.

## Gotchas
- Blurring albedo washes out texture: divide albedo out before the blur and multiply back after (or split
  texturing pre/post scatter, sqrt on each side).
- Without depth weights skin bleeds onto hair and background.
- Scattering distance must be in world units consistent with scene scale.

## Verify
- [ ] Back-lit ear glows red; the face terminator softens with a warm tint; no halo against the background.
- [ ] Side by side with a path-traced random-walk reference at matching albedo and mean free path.
