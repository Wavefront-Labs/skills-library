---
id: computing-software.computer-graphics-engineering.rendering-techniques.openxr-frame-loop
name: openxr-frame-loop
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, vr-rendering, xr-rendering, openxr, xrwaitframe, xrbeginframe, xrendframe, xrlocateviews, predicted-display-time, swapchain-images, session-state]
level: advanced
status: docs-checked
description: "Drive an OpenXR render loop correctly: session state machine, xrWaitFrame/BeginFrame/EndFrame pacing, predicted display time for xrLocateViews."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters", "https://github.com/KhronosGroup/OpenXR-SDK-Source/tree/main/src/tests/hello_xr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenXR frame loop

**Goal:** a native VR/AR renderer that the runtime can pace and reproject correctly on
any conformant OpenXR runtime.

## 1. Session state machine
Poll `xrPollEvent` every frame; handle `XR_TYPE_EVENT_DATA_SESSION_STATE_CHANGED`:
| state | action |
|---|---|
| READY | `xrBeginSession` (set `primaryViewConfigurationType`, here PRIMARY_STEREO) |
| SYNCHRONIZED / VISIBLE / FOCUSED | keep running the frame loop; the session receives XR input only in FOCUSED |
| STOPPING | leave the render loop, then `xrEndSession` (session returns to IDLE) |
| EXITING | release session resources, `xrDestroySession`, end the process if there is no non-XR experience |
| LOSS_PENDING | `xrDestroySession`; optionally poll `xrGetSystem` and create a new session |
`xrBeginSession` outside READY returns `XR_ERROR_SESSION_NOT_READY`; `xrEndSession` outside STOPPING returns `XR_ERROR_SESSION_NOT_STOPPING`.

## 2. The frame
```cpp
XrFrameState fs{XR_TYPE_FRAME_STATE};
xrWaitFrame(session, nullptr, &fs);          // blocks to pace the app to the display
xrBeginFrame(session, nullptr);
std::vector<XrCompositionLayerProjectionView> views(2, {XR_TYPE_COMPOSITION_LAYER_PROJECTION_VIEW});
if (fs.shouldRender) {
    XrViewLocateInfo li{XR_TYPE_VIEW_LOCATE_INFO, nullptr, XR_VIEW_CONFIGURATION_TYPE_PRIMARY_STEREO,
                        fs.predictedDisplayTime, appSpace};
    XrViewState vs{XR_TYPE_VIEW_STATE}; uint32_t n; XrView xv[2]{{XR_TYPE_VIEW}, {XR_TYPE_VIEW}};
    xrLocateViews(session, &li, &vs, 2, &n, xv);   // poses + asymmetric FOVs for that display time
    for (int eye = 0; eye < 2; ++eye) {
        uint32_t idx; xrAcquireSwapchainImage(sc[eye], nullptr, &idx);
        XrSwapchainImageWaitInfo wi{XR_TYPE_SWAPCHAIN_IMAGE_WAIT_INFO, nullptr, XR_INFINITE_DURATION};
        xrWaitSwapchainImage(sc[eye], &wi);
        renderEye(images[eye][idx], xv[eye].pose, xv[eye].fov);   // asymmetric projection from fov angles
        xrReleaseSwapchainImage(sc[eye], nullptr);
        views[eye].pose = xv[eye].pose; views[eye].fov = xv[eye].fov;
        views[eye].subImage = {sc[eye], {{0, 0}, {w, h}}, 0};
    }
}
XrCompositionLayerProjection layer{XR_TYPE_COMPOSITION_LAYER_PROJECTION};
layer.space = appSpace; layer.viewCount = 2; layer.views = views.data();
const XrCompositionLayerBaseHeader* layers[] = {(XrCompositionLayerBaseHeader*)&layer};
XrFrameEndInfo ei{XR_TYPE_FRAME_END_INFO, nullptr, fs.predictedDisplayTime,
                  XR_ENVIRONMENT_BLEND_MODE_OPAQUE, fs.shouldRender ? 1u : 0u, layers};
xrEndFrame(session, &ei);
```
- While the session is running keep calling Wait/Begin/End even when `shouldRender` is false: skip rendering and omit the layers from `xrEndFrame` (the spec says to keep the frame loop going to stay synchronised).
- Use `predictedDisplayTime` for view poses **and** for controller poses (`xrLocateSpace`) so
  everything is predicted to the same photon time.
- Submit the exact pose/FOV you rendered with; the spec stresses an accurate display time to avoid reprojection artefacts.

## 3. Projection from XrFovf
Build an asymmetric frustum from `angleLeft/Right/Up/Down` (tangents); don't assume symmetric
FOV or a shared projection for both eyes.

## 4. Extras
- Depth submission (`XR_KHR_composition_layer_depth`) lets the runtime make more accurate reprojections.
- Single swapchain with 2 array layers + multiview instead of 2 swapchains.
- Quad layers (core `XrCompositionLayerQuad`) for UI and text, composed by the runtime instead of baked into the eye buffers.

## Gotchas
- Call `xrBeginFrame` right before executing graphics device work for the frame, not after it; `xrWaitFrame` is where throttling happens, not `xrBeginFrame`.
- Reference space choice: STAGE vs LOCAL (a world-locked, gravity-aligned origin); handle
  `XR_TYPE_EVENT_DATA_REFERENCE_SPACE_CHANGE_PENDING` (recentering).

## Verify
- [ ] Session lifecycle (headset off/on, app switch) handled without errors.
- [ ] Controllers align with hands (same predicted time used).

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16, API 1.1.65). Confirmed against session.adoc: state machine, xrBeginSession only in READY and xrEndSession only in STOPPING, FOCUSED receives input, EXITING and LOSS_PENDING handling. Confirmed against rendering.adoc: XrFrameState fields, shouldRender false means keep the loop running with layers omitted, xrWaitFrame blocks and xrBeginFrame must not throttle, predictedDisplayTime is the display midpoint, XrFrameEndInfo members, layer count limit. Removed the headset vendor list, the CPU-work latency advice and the performance overlay check because no specification text backs them.

Method: documentation only; no commands were run.
