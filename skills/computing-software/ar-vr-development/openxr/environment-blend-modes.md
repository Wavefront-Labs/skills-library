---
id: computing-software.ar-vr-development.openxr.environment-blend-modes
name: environment-blend-modes
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-blend-modes-passthrough, environment-blend-modes]
level: practitioner
status: docs-checked
description: "Choose OPAQUE, ADDITIVE or ALPHA_BLEND for the display type."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Select an environment blend mode
**Goal:** Choose OPAQUE, ADDITIVE or ALPHA_BLEND for the display type.

- `xrEnumerateEnvironmentBlendModes` for the view configuration; pass the chosen mode in `XrFrameEndInfo::environmentBlendMode`.
- OPAQUE is the typical VR mode. ADDITIVE is typical for see-through headsets with an additive display; black composited pixels appear transparent and alpha is ignored.
- ALPHA_BLEND is typical for a phone or headset with video passthrough; the composited alpha channel sets each pixel's blend with the real world.

## Gotchas
- Layer alpha handling follows the layer flags: `XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT` and `XR_COMPOSITION_LAYER_UNPREMULTIPLIED_ALPHA_BIT`.

## Self-check
Real world visible through transparent pixels in mixed reality mode.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter (blend mode enumerants, composition layer blending flags). Removed: the instruction to clear alpha to 0 (not stated in those words).

Method: documentation only; no commands were run.
