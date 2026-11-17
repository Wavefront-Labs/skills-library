---
id: computing-software.ar-vr-development.openxr.api-layers-validation
name: api-layers-validation
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, api-layers-validation]
level: practitioner
status: docs-checked
description: "Insert an OpenXR API layer, such as the core validation layer, between app and runtime."
sources:
  - https://github.com/KhronosGroup/OpenXR-SDK-Source/tree/main/specification/loader
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use API layers for validation
**Goal:** Insert an OpenXR API layer, such as a validation layer, between app and runtime.

- Layers are discovered through JSON manifest files; the loader reads explicit-layer locations (for example `openxr/1/api_layers/explicit.d` directories on Linux) and any paths in `XR_API_LAYER_PATH`.
- Request layers by name in `XrInstanceCreateInfo::enabledApiLayerNames`; list available ones with `xrEnumerateApiLayerProperties`. The `XR_ENABLE_API_LAYERS` environment variable (colon separated on Linux, semicolon on Windows) can force layers on without code changes.
- The loader docs note that validation is a common use of layers and that its overhead disappears when the layer is not loaded.

## Gotchas
- An implicit layer found by the loader loads by default unless overridden; explicit layers must be requested.

## Self-check
`xrEnumerateApiLayerProperties` lists the layer you installed.

## Checked

Date: 2026-11-02. Confirmed in the loader API-layer and application chapters and the instance chapter. Removed: the XR_APILAYER_LUNARG_core_validation name (only a test layer name appears in the docs), the xrBeginFrame-before-xrWaitFrame self-check, 'never ship enabled'.

Method: documentation only; no commands were run.
