---
id: computing-software.ar-vr-development.openxr.system-form-factor
name: system-form-factor
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, xr-system-and-view-config, system-form-factor]
level: practitioner
status: docs-checked
description: "Pick the XR device with xrGetSystem using the right form factor."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Get an XrSystemId for a form factor
**Goal:** Pick the XR device with xrGetSystem using the right form factor.

- Fill `XrSystemGetInfo::formFactor` with `XR_FORM_FACTOR_HEAD_MOUNTED_DISPLAY` or `XR_FORM_FACTOR_HANDHELD_DISPLAY`.
- `XR_ERROR_FORM_FACTOR_UNAVAILABLE` means the form factor is supported but temporarily unavailable; a later call may succeed, so retry rather than exit.
- Query `xrGetSystemProperties` for `maxSwapchainImageWidth`/`Height` and tracking properties (`orientationTracking`, `positionTracking`).

## Self-check
Properties report positionTracking true on a 6DoF headset.

## Checked

Date: 2026-11-02. Confirmed in the system chapter. Removed: 'a system id is only valid for the instance that produced it' wording beyond the doc and the connect-headset message.

Method: documentation only; no commands were run.
