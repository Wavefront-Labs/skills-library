---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-composition-layers-and-depth-submission
name: xr-composition-layers-and-depth-submission
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, composition-layers, openxr, depth-submission, quad-layer, positional-timewarp]
level: advanced
status: docs-checked
description: "Submit OpenXR composition layers well: projection plus quad/cylinder layers, layer ordering and flags, and XR_KHR_composition_layer_depth for positional reprojection."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/khr/khr_composition_layer_depth.adoc", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/fb/fb_space_warp.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XR composition layers and depth submission

## 1. Layer stack in xrEndFrame
```c
const XrCompositionLayerBaseHeader* layers[] = {
  (XrCompositionLayerBaseHeader*)&projectionLayer,   // layer 0 is drawn first
  (XrCompositionLayerBaseHeader*)&menuQuadLayer };
XrFrameEndInfo end = { XR_TYPE_FRAME_END_INFO };
end.displayTime = frameState.predictedDisplayTime;
end.environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_OPAQUE;
end.layerCount = 2; end.layers = layers;
xrEndFrame(session, &end);
```
Core types: projection (per-eye stereo), quad (flat panel in a space). Extensions: cylinder,
equirect, cube (`XR_KHR_composition_layer_*`), passthrough (`XR_FB_passthrough`). A conformant runtime
supports at least `XR_MIN_COMPOSITION_LAYERS_SUPPORTED` (16) layers; read the real limit from
`XrSystemGraphicsProperties::maxLayerCount`. All layers are drawn in array order with a painter's algorithm,
and every layer you want visible must be resubmitted in every `xrEndFrame`.

## 2. Quad/cylinder layers for UI and video
- Composed by the runtime compositor instead of being baked into the eye buffers.
- Own swapchain, so it can be redrawn less often: the image referenced is the last one you released, so an unchanged panel only needs to be resubmitted in the layer list.
- Place in `LOCAL`/`STAGE` space for world-locked, `VIEW` space for head-locked (sparingly).
- Flags: `XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT` to use the texture alpha (otherwise alpha is 1),
  `XR_COMPOSITION_LAYER_UNPREMULTIPLIED_ALPHA_BIT` if the colour is not premultiplied. The
  `CORRECT_CHROMATIC_ABERRATION_BIT` flag is deprecated and has no effect on known conformant runtimes.
- Layers do not depth-test against each other or your 3D scene (painter's algorithm, and depth
  submission does not change composition order); to show 3D objects in front of a quad, order the layers
  accordingly or draw the panel into the scene.

## 3. Depth submission (XR_KHR_composition_layer_depth)
Chain an `XrCompositionLayerDepthInfoKHR` to each projection view: depth swapchain image,
`minDepth/maxDepth` (window-space, within [0, 1], minDepth < maxDepth), `nearZ/farZ` (positive metres in
(0, +inf], must differ; `nearZ > farZ` describes reversed depth). The runtime may use it for more accurate
reprojection. `XR_FB_space_warp` is independent of this extension: it takes its own motion-vector image and
a separate, usually lower-resolution depth image per view (`XrCompositionLayerSpaceWarpInfoFB`).

## 4. Swapchain details
Allocate swapchains with formats from `xrEnumerateSwapchainFormats` ; acquire/wait/release each frame for each swapchain you update; the same swapchain may be referenced by several
layers with different image rectangles; array swapchains (`arraySize = 2`) pair with multiview rendering.

## Gotchas
- nearZ/farZ and min/maxDepth in the depth info must describe the depth buffer you actually rendered.
- A layer that references a swapchain with no released image fails with `XR_ERROR_LAYER_INVALID`; exceeding `maxLayerCount` fails with `XR_ERROR_LAYER_LIMIT_EXCEEDED`; image rects outside the swapchain give `XR_ERROR_SWAPCHAIN_RECT_INVALID`.

## Verify
- [ ] `xrEndFrame` returns success with every layer you expect (check the error codes above).

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16, API 1.1.65). Confirmed: XR_MIN_COMPOSITION_LAYERS_SUPPORTED is 16 (xr.xml) and maxLayerCount; painter's-algorithm ordering with the 0th layer first; composition-layer flag bits and the deprecated chromatic-aberration flag (xr.xml comment); XrCompositionLayerDepthInfoKHR ranges and reversed depth via nearZ greater than farZ; XR_FB_space_warp is independent of the KHR depth extension and has its own depth image; layer error codes. Removed the claims about sharper quad text, runtime depth-composited layers, positional timewarp and compositor cost, which no specification text states.

Method: documentation only; no commands were run.
