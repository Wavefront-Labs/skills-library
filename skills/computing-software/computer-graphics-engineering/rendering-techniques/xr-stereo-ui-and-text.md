---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-stereo-ui-and-text
name: xr-stereo-ui-and-text
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, stereo-ui, vr-text, angular-size, vergence-accommodation, world-space-ui]
level: advanced
status: gated
description: "Design and render readable UI in stereo XR: world-space placement and distances, angular text sizing, SDF text, avoiding depth conflicts and head-locked HUDs, and using layers."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/rendering.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI and text in stereo XR

## 1. Screen-space UI does not exist
A 2D overlay drawn identically to both eyes appears at infinity while the world is closer:
eye strain and double images. Put UI in the world: panels at a real depth, rendered per eye like geometry.

## 2. Placement
- Comfortable distance 0.75-3 m (gated: unconfirmed, source is paywalled or blocked); most headsets
  focus around 1.3-2 m (gated: unconfirmed, source is paywalled or blocked). Interactive panels within arm's reach (~0.5-0.7 m) for direct touch (gated: unconfirmed, source is paywalled or blocked).
- Keep primary content within ~30 degrees of forward gaze, slightly below eye level (gated: unconfirmed, source is paywalled or blocked); curve
  wide panels around the user (cylinder) so edges stay equidistant.
- Head-locked UI only for brief, minimal notices; prefer lazy-follow (body-locked, eases to
  follow when the user turns past a threshold).

## 3. Text sizing by angle
Size by visual angle, not pixels: height = 2 * d * tan(angle/2).
A practical floor for body text is about 1 degree of visual angle for the line height (about
17.5 mm at 1 m, 35 mm at 2 m, by the formula; the 1 degree floor itself is gated: unconfirmed, source is paywalled or blocked); titles larger. Platform guides (Meta, Microsoft, Apple visionOS)
publish their own minimums; confirm on the target headset.
Check panel PPD (pixels per degree): low PPD means thin fonts alias; use medium/bold weights.

## 4. Rendering text
- SDF/MSDF text (troika, TextMeshPro) stays sharp at any distance; enable mipmaps/supersampling to avoid shimmer.
- Moderate contrast and a slight dark backplate behind text; the smearing rationale for avoiding pure white on black is gated: unconfirmed, source is paywalled or blocked.
- Render UI into a compositor quad or cylinder layer (`XrCompositionLayerQuad`, `XR_KHR_composition_layer_cylinder`) instead of the eye buffers; the runtime composes layers in array order.

## 5. Depth conflicts
UI must never be occluded inconsistently: if a world object passes in front of a panel it should
truly occlude it (depth test on) or the panel should be moved; rendering UI on top with depth off
while it is "behind" an object creates painful conflicts. Raycast pointers should end on the
panel surface with a visible cursor.

## Gotchas
- Thin 1-px lines and small icons flicker with head micro-motion; use >= 2 px strokes (gated: unconfirmed, source is paywalled or blocked).
- Text that billboards every frame jitters with tracking noise; billboard with damping or only on yaw.

## Verify
- [ ] Body text readable at its intended distance by someone not wearing glasses correction.
- [ ] No double images when focusing between UI and the scene behind it.

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16). Confirmed: quad and cylinder composition layers exist (core quad, XR_KHR_composition_layer_cylinder) and layers compose in array order; the visual-angle arithmetic (2 x d x tan(angle/2), 17.5 mm at 1 m and 34.9 mm at 2 m for 1 degree) was computed. The ergonomic distances, angles, minimum text size, PPD and stroke-width guidance come from vendor design guides (Meta, Apple) that could not be read as plain documentation, so they are marked gated.

Method: documentation only; no commands were run.
