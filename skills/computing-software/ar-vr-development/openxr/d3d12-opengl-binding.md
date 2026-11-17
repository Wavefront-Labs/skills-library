---
id: computing-software.ar-vr-development.openxr.d3d12-opengl-binding
name: d3d12-opengl-binding
category: computing-software
field: ar-vr-development
product: openxr
tags: [openxr, d3d12-opengl-binding]
level: practitioner
status: docs-checked
description: "Use the matching *_enable extension and requirements call for D3D or OpenGL."
sources:
  - https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind D3D11/D3D12/OpenGL
**Goal:** Use the matching *_enable extension and requirements call for D3D or OpenGL.

- `XR_KHR_D3D11_enable`, `XR_KHR_D3D12_enable`, `XR_KHR_opengl_enable`, `XR_KHR_opengl_es_enable`; each defines a graphics requirements query (D3D: adapter LUID and minimum feature level).
- Create your device on the adapter named by the requirements (`adapterLuid`).
- Swapchain image structs are API-specific, for example `XrSwapchainImageD3D11KHR`.

## Gotchas
- A device that does not satisfy the requirements can be rejected with `XR_ERROR_GRAPHICS_DEVICE_INVALID`.

## Self-check
xrCreateSession succeeds on the same GPU the headset is attached to.

## Checked

Date: 2026-11-02. Confirmed in the four enable extension pages: names, requirements query, adapterLuid, minFeatureLevel, GRAPHICS_DEVICE_INVALID. Removed: 'LUID must match or session creation fails' stated as such (the page gives the device-invalid error).

Method: documentation only; no commands were run.
