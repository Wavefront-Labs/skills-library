---
id: computing-software.ar-vr-development.openxr.passthrough-extensions
name: passthrough-extensions
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, passthrough-extensions]
level: advanced
status: docs-checked
description: "Enable vendor passthrough layers where the standard blend mode is not offered."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/blob/main/specification/registry/xr.xml
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable vendor passthrough
**Goal:** Use a vendor passthrough extension where the standard blend mode is not enough.

- `XR_FB_passthrough` is a registered instance extension; its structures and setup are defined on its own extension page.
- Standard path: `XR_ENVIRONMENT_BLEND_MODE_ALPHA_BLEND` on devices with video passthrough; check support at runtime and keep an opaque fallback.

## Self-check
App starts in VR-only mode on a runtime lacking the extension, without errors.

## Checked

Date: 2026-11-02. Confirmed: XR_FB_passthrough exists in the registry, ALPHA_BLEND meaning in the rendering chapter. Removed: Meta/Pico vendor claims and release-to-release change remarks.

Method: documentation only; no commands were run.
