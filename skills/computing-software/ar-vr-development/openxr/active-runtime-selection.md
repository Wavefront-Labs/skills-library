---
id: computing-software.ar-vr-development.openxr.active-runtime-selection
name: active-runtime-selection
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, active-runtime-selection]
level: practitioner
status: docs-checked
description: "Find which runtime the loader will use and override it for testing."
sources:
  - https://github.com/KhronosGroup/OpenXR-SDK-Source/tree/main/specification/loader
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Select and verify the active OpenXR runtime
**Goal:** Find which runtime the loader will use and override it for testing.

- The loader reads an active runtime manifest (JSON naming the runtime library). On Windows the location is in the registry under `HKEY_LOCAL_MACHINE\SOFTWARE\Khronos\OpenXR\<major_api_version>`, value `ActiveRuntime`. On Linux it is `active_runtime.json` (or `active_runtime.<arch>.json`) under `openxr/<major_api_version>` in an XDG configuration directory or the system config directory (typically `/etc`).
- Override with the `XR_RUNTIME_JSON` environment variable pointing at a runtime manifest; when it is set the loader does not search the default locations.

## Gotchas
- Switching runtimes changes which extensions exist; re-run feature detection.

## Self-check
`xrGetInstanceProperties` returns the runtime name and version you expect.

## Checked

Date: 2026-11-02. Confirmed in the loader runtime chapter: registry key and ActiveRuntime value, Linux file names and search directories, XR_RUNTIME_JSON override. Removed: vendor-app 'set as active runtime' button claim (not in the docs).

Method: documentation only; no commands were run.
