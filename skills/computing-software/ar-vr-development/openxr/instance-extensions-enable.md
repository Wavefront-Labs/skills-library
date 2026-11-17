---
id: computing-software.ar-vr-development.openxr.instance-extensions-enable
name: instance-extensions-enable
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-instance-and-loader, instance-extensions-enable]
level: practitioner
status: docs-checked
description: "Enumerate runtime extensions, then request only those you need in xrCreateInstance."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable extensions when creating an XrInstance
**Goal:** Enumerate runtime extensions, then request only those you need in xrCreateInstance.

- Call `xrEnumerateInstanceExtensionProperties` with the two-call idiom (capacity 0 first, then allocate) and compare names such as `XR_KHR_vulkan_enable2` against what you need.
- Put the chosen names in `XrInstanceCreateInfo::enabledExtensionNames`; set `XrApplicationInfo::apiVersion` to `XR_API_VERSION_1_0` or `XR_API_VERSION_1_1` (the spec calls these useful values).
- Check calls with `XR_SUCCEEDED(result)`; creation fails with `XR_ERROR_EXTENSION_NOT_PRESENT` if a requested extension is missing.

## Gotchas
- Extensions are optional and must be enabled by the application; extension function pointers come from `xrGetInstanceProcAddr`.

## Self-check
Log the enabled extension list at startup and confirm xrCreateInstance returns XR_SUCCESS.

## Checked

Date: 2026-11-02. Confirmed in the instance, API initialization and fundamentals chapters and the registry. Fixed: apiVersion belongs to XrApplicationInfo, not applicationInfo.apiVersion shorthand. Removed: the XR_MAKE_VERSION(1, 0, 0) example, XR_FB_*/XR_META_* vendor-only claims.

Method: documentation only; no commands were run.
