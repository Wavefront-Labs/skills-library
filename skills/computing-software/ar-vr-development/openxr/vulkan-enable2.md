---
id: computing-software.ar-vr-development.openxr.vulkan-enable2
name: vulkan-enable2
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-graphics-bindings, vulkan-enable2]
level: advanced
status: docs-checked
description: "Let the runtime choose the Vulkan instance, physical device and extensions."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind Vulkan with XR_KHR_vulkan_enable2
**Goal:** Let the runtime choose the Vulkan instance, physical device and extensions.

- Use `xrCreateVulkanInstanceKHR` and `xrCreateVulkanDeviceKHR`, then `xrGetVulkanGraphicsDevice2KHR`.
- Get requirements via `xrGetVulkanGraphicsRequirements2KHR` (`minApiVersionSupported`, `maxApiVersionSupported`).
- Pass `XrGraphicsBindingVulkan2KHR` with `queueFamilyIndex` and `queueIndex`.

## Gotchas
- `XR_KHR_vulkan_enable2` is an alternative to `XR_KHR_vulkan_enable`; use one.

## Self-check
Session creation succeeds with the device returned by the runtime.

## Checked

Date: 2026-11-02. Confirmed in the XR_KHR_vulkan_enable2 page. Removed: validation-layer self-check.

Method: documentation only; no commands were run.
