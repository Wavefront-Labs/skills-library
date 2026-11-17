---
id: computing-software.ar-vr-development.openxr.quad-cylinder-layers
name: quad-cylinder-layers
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, quad-cylinder-layers]
level: practitioner
status: docs-checked
description: "Render UI and video as quad or cylinder layers for sharper text."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use quad and cylinder layers for UI
**Goal:** Render UI and video as quad or cylinder layers.

- `XrCompositionLayerQuad` places a texture in a space with a size in meters; `XR_KHR_composition_layer_cylinder` curves it.
- Set `eyeVisibility` and `layerFlags` (for example the blend-texture-source-alpha bit).

## Gotchas
- Layers are drawn in submission order with a painter's algorithm.

## Self-check
The quad appears at the size and pose set in the layer.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter and the cylinder extension page. Removed: the claim of crisper text than eye buffers and the no-depth-test wording.

Method: documentation only; no commands were run.
