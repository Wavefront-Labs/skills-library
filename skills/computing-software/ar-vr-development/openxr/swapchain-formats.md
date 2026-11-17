---
id: computing-software.ar-vr-development.openxr.swapchain-formats
name: swapchain-formats
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-swapchains, swapchain-formats]
level: practitioner
status: docs-checked
description: "Choose a colour and depth format from what the runtime supports."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pick a swapchain format
**Goal:** Choose a colour and depth format from what the runtime supports.

- `xrEnumerateSwapchainFormats` returns native API format ids ordered highest to lowest runtime preference; use the highest-preference format you support.
- Content meant to be sRGB must use an API-specific sRGB format (for example `DXGI_FORMAT_R8G8B8A8_UNORM_SRGB`, `GL_SRGB8_ALPHA8`, `VK_FORMAT_R8G8B8A8_SRGB`).
- Set `usageFlags` such as `XR_SWAPCHAIN_USAGE_COLOR_ATTACHMENT_BIT` and `sampleCount` in `XrSwapchainCreateInfo`.

## Gotchas
- Format ids are API-specific numbers, not portable.

## Self-check
The chosen format appears in the list returned by the runtime.

## Checked

Date: 2026-11-02. Confirmed in the rendering chapter (format preference order, sRGB formats, create info fields).

Method: documentation only; no commands were run.
