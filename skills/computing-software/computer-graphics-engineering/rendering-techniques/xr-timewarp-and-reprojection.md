---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-timewarp-and-reprojection
name: xr-timewarp-and-reprojection
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, timewarp, asynchronous-reprojection, spacewarp, openxr, motion-to-photon]
level: sme
status: docs-checked
description: "Work with XR timewarp and asynchronous reprojection: predicted poses, depth and motion-vector submission for spacewarp, and avoiding judder."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/khr/khr_composition_layer_depth.adoc", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/fb/fb_space_warp.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timewarp and reprojection

## 1. What the runtime does
Reprojection is runtime behaviour, not something OpenXR makes you implement. The spec notes that an accurate predicted
display time avoids black pull-in by reprojection and reduces judder when a runtime lacks translational reprojection, and that
reprojection must not show frames before the display period they were predicted for.
- **Rotational timewarp (ATW)**: re-projects the submitted eye images by the difference between the pose you rendered
  with and a newer pose. Hides rotational latency; cannot fix translation parallax or animation.
- **Positional reprojection**: with submitted depth (`XR_KHR_composition_layer_depth`) the runtime may reproject more accurately.
- **Frame extrapolation (`XR_FB_space_warp`)**: given an application motion-vector image and a depth image, the runtime
  can extrapolate frames so the app renders at half rate.

## 2. What the app must do (OpenXR)
```c
xrWaitFrame(session, &waitInfo, &frameState);            // gives predictedDisplayTime
xrBeginFrame(session, &beginInfo);
xrLocateViews(session, &(XrViewLocateInfo){ .displayTime = frameState.predictedDisplayTime, .space = stageSpace, ... }, ...);
// render with exactly these view poses and fovs
// submit projection views with the same pose/fov you rendered with
xrEndFrame(session, &endInfo);                            // displayTime = predictedDisplayTime
```
- Render with the predicted pose for `predictedDisplayTime`, and submit that same pose in
  `XrCompositionLayerProjectionView`; a mismatch makes the world swim.
- Chain `XrCompositionLayerDepthInfoKHR` (`XR_KHR_composition_layer_depth`) with near/far to every projection view for more
  accurate reprojection; for space warp add `XrCompositionLayerSpaceWarpInfoFB` (`XR_FB_space_warp`) with its own motion-vector
  and depth sub-images (independent of the KHR depth image, usually lower resolution).
- Lock controllers/hands to the same predicted time as the head.

## 3. Content rules
- Head-locked HUDs: submit as a separate quad layer in `XR_REFERENCE_SPACE_TYPE_VIEW` rather than baking them into the eye buffer.
- Text and UI on quad/cylinder composition layers are composed by the runtime, not by your eye-buffer pass.
- Transparent and particle effects have no natural motion vectors for space warp; write motion for them or keep them minimal.
  `XR_COMPOSITION_LAYER_SPACE_WARP_INFO_FRAME_SKIP_BIT_FB` lets you skip extrapolation for a frame that suits it badly.

## Gotchas
- Re-querying the pose late in the frame and rendering with it but submitting the earlier pose gives a pose mismatch: submit the pose you rendered with.
- Depth info must match the buffer: `nearZ`/`farZ` are positive metres in (0, +inf] and must differ, `nearZ > farZ` encodes reversed depth,
  `minDepth < maxDepth` within [0, 1].

## Verify
- [ ] Shaking head while looking at a world-locked grid shows no swimming; head-locked UI stable.

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16). Confirmed: xrEndFrame note on predicted display time and reprojection (rendering.adoc), XrCompositionLayerDepthInfoKHR semantics and ranges, XR_FB_space_warp motion-vector and separate depth inputs and the frame-skip flag, XR_REFERENCE_SPACE_TYPE_VIEW. Removed the vendor product list (AppSW, SteamVR, WMR), the claim that doubled images persist below refresh rate even with warping, and the wobble claim for baked head-locked HUDs, which no documentation states.

Method: documentation only; no commands were run.
