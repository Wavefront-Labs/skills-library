---
id: computing-software.ar-vr-development.openxr.view-configuration-types
name: view-configuration-types
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, view-configuration-types]
level: practitioner
status: docs-checked
description: "Enumerate view configurations and recommended per-eye resolution."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose a view configuration
**Goal:** Enumerate view configurations and recommended per-eye resolution.

- `xrEnumerateViewConfigurations` lists types such as `XR_VIEW_CONFIGURATION_TYPE_PRIMARY_MONO` and `PRIMARY_STEREO`.
- `xrEnumerateViewConfigurationViews` returns `recommendedImageRectWidth`, `recommendedImageRectHeight`, the max values and `recommendedSwapchainSampleCount` per view; allocate swapchains from the recommended size.
- `PRIMARY_STEREO_WITH_FOVEATED_INSET` adds foveated inset views; the structures that configure it are not defined in core OpenXR.

## Self-check
Swapchain size equals the recommended size times any supersampling factor you chose.

## Checked

Date: 2026-11-02. Confirmed in the view configurations chapter. Removed: the GPU-cost remark, and the 'quad-view is an extension' wording (replaced with what the chapter says).

Method: documentation only; no commands were run.
