---
id: computing-software.ar-vr-development.openxr.projection-layer-depth
name: projection-layer-depth
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-composition-layers, projection-layer-depth]
level: practitioner
status: docs-checked
description: "Submit the stereo view as a projection layer and optionally supply depth."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submit a projection layer with depth
**Goal:** Submit the stereo view as a projection layer and optionally supply depth.

- `XrCompositionLayerProjection` with one `XrCompositionLayerProjectionView` per eye (subImage, pose, fov).
- Chain `XrCompositionLayerDepthInfoKHR` (`XR_KHR_composition_layer_depth`) with `nearZ`/`farZ` so the runtime can take depth into account in reprojection; nearZ and farZ must not be equal.
- Pass layers in `XrFrameEndInfo::layers`; they are drawn in the order given.

## Self-check
Depth info is accepted by xrEndFrame with no validation errors.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter and the composition layer depth page. Removed: 'wrong values degrade reprojection' and the timewarp edge-smear self-check.

Method: documentation only; no commands were run.
