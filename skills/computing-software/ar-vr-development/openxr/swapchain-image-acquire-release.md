---
id: computing-software.ar-vr-development.openxr.swapchain-image-acquire-release
name: swapchain-image-acquire-release
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, swapchain-image-acquire-release]
level: practitioner
status: docs-checked
description: "Use the three-step image protocol every frame."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acquire, wait and release swapchain images
**Goal:** Use the three-step image protocol every frame.

- `xrAcquireSwapchainImage`, then `xrWaitSwapchainImage` with a timeout in nanoseconds (`XR_TIMEOUT_EXPIRED` if it elapses), render, then `xrReleaseSwapchainImage`.
- Enumerate images with `xrEnumerateSwapchainImages` and index by the acquired index.
- Swapchain images can be 2D or 2D array; `imageArrayIndex` in the sub-image must be below the swapchain's `arraySize`.

## Gotchas
- The image must be waited on without timeout before release; `xrEndFrame` uses the most recently released image.

## Self-check
No call-order errors from the runtime.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter. Removed: 'enumerate once', one-array-for-both-eyes advice, and 'release every image before xrEndFrame' (spec says xrEndFrame uses the most recently released image).

Method: documentation only; no commands were run.
