---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-lens-distortion-correction
name: xr-lens-distortion-correction
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, lens-distortion-correction, chromatic-aberration-correction, barrel-distortion, distortion-mesh]
level: advanced
status: docs-checked
description: "Pre-distort XR eye images for headset lenses: barrel distortion models, per-channel chromatic correction, distortion meshes vs per-pixel, render scale and who owns the step."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/view_configurations.adoc", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/rendering.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lens distortion and chromatic correction for XR

## 1. Who does it
In OpenXR the runtime compositor performs distortion correction (and frame-rate interpolation): you submit
undistorted eye images as composition layers. You only need this when
building a runtime/compositor, custom hardware (DIY headsets, Cardboard-style viewers), or
offline previews. Knowing it still matters for render-scale and FOV decisions.

## 2. The model
Headset lenses magnify with pincushion distortion; the image is pre-warped with the inverse
(barrel). Radial polynomial in normalised lens-centred coordinates:
```
r2 = x*x + y*y
scale = 1 + k1*r2 + k2*r2*r2 (+ k3*r2^3)
src = center + (p - center) * scale        // per eye, lens centre may be off image centre
```
Coefficients come from the lens design or a calibration.

## 3. Chromatic aberration correction
Lenses refract red less than blue, so colours separate towards the edges. Sample each channel
with its own scale (or separate k coefficients per channel), fitted from calibration. Three texture fetches per pixel.
In OpenXR do not rely on `XR_COMPOSITION_LAYER_CORRECT_CHROMATIC_ABERRATION_BIT`: it is deprecated and has no effect on known conformant runtimes.

## 4. Implementation options
- **Distortion mesh**: a grid per eye with precomputed per-vertex R/G/B UVs, evaluating the polynomial per vertex
  instead of per pixel.
- **Per-pixel shader**: simple, flexible for calibration tools, slower.

## 5. Render scale
Barrel pre-warp compresses the periphery and stretches the centre, so the eye buffer size is a runtime
decision. Use `recommendedImageRectWidth`/`Height` from `xrEnumerateViewConfigurationViews`
(`XrViewConfigurationView`) as the starting size instead of the panel resolution.

## Gotchas
- Do not apply distortion yourself when submitting to OpenXR: the runtime already corrects it, so you would distort twice.
- Sample with clamp-to-border black; out-of-range UVs otherwise smear edge pixels.

## Verify
- [ ] Grid test pattern appears straight through the lenses across the full FOV.
- [ ] No colour fringing on white text near the edge.

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16). Confirmed in rendering.adoc that the runtime compositor performs distortion correction and frame-rate interpolation for composition layers; recommendedImageRectWidth is in XrViewConfigurationView (view_configurations.adoc); the chromatic-aberration layer flag is deprecated with no effect (xr.xml). Removed the fixed 1.3-1.4x render-scale figure, the 40x40 mesh size, the per-channel sign convention, the OpenCV equivalence, and the WebXR/Quest/SteamVR claims. The radial polynomial is presented as a generic model, not a specification.

Method: documentation only; no commands were run.
