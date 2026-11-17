---
id: computing-software.ar-vr-development.openxr.debug-utils-messenger
name: debug-utils-messenger
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-conformance-and-debug, debug-utils-messenger]
level: practitioner
status: docs-checked
description: "Receive runtime diagnostics and name objects for debugging."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add an XR_EXT_debug_utils messenger
**Goal:** Receive runtime diagnostics and name objects for debugging.

- Enable `XR_EXT_debug_utils`, create a messenger with `xrCreateDebugUtilsMessengerEXT` and a callback and severity/type mask.
- Name objects with `xrSetDebugUtilsObjectNameEXT` so messages are readable.

## Gotchas
- The extension is optional; check it is enumerated before enabling it.

## Self-check
Messages show named swapchains and sessions.

## Checked

Date: 2026-11-02. Confirmed in the XR_EXT_debug_utils page. Removed: the advice to log at VERBOSE only in development.

Method: documentation only; no commands were run.
