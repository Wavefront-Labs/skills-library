---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-device-and-canvas-setup
name: webgpu-device-and-canvas-setup
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, wgsl, requestadapter, gpu-device-limits, requestdevice, getpreferredcanvasformat, canvas-configure, required-features, device-lost, error-scopes]
level: practitioner
status: docs-checked
description: "Initialise raw WebGPU robustly: feature detection, requesting only needed limits and features, preferred canvas format, labels, resize and device loss."
sources: ["https://webgpufundamentals.org/webgpu/lessons/webgpu-fundamentals.html", "https://webgpufundamentals.org/webgpu/lessons/webgpu-limits-and-features.html", "https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebGPU device and canvas setup

**Goal:** a WebGPU app that starts on every supporting browser, asks for exactly what it
needs, survives device loss, and reports errors usefully.

## 1. Detect and request
```js
if (!navigator.gpu) return fallbackToWebGL2();
const adapter = await navigator.gpu.requestAdapter();
if (!adapter) return fallbackToWebGL2();                // no usable GPU
const want = ['timestamp-query', 'shader-f16'].filter(f => adapter.features.has(f));
const device = await adapter.requestDevice({
  requiredFeatures: want,
  requiredLimits: {                                      // ask only for above-default limits you need
    maxStorageBufferBindingSize: Math.min(adapter.limits.maxStorageBufferBindingSize, 512 << 20),
  },
});
```
The adapter represents a specific GPU (some devices have several). Limits and features are
requested through `requiredLimits` and `requiredFeatures`; if the request cannot be met,
`requestDevice` rejects. Request only what you use.

## 2. Canvas
```js
const ctx = canvas.getContext('webgpu');
const format = navigator.gpu.getPreferredCanvasFormat();
ctx.configure({ device, format });
// each frame:
const view = ctx.getCurrentTexture().createView();
```
- Canvases default to 300x150 pixels. Resize with a `ResizeObserver`: set `canvas.width/height`
  from the observed size, clamped to `device.limits.maxTextureDimension2D`, and re-render. The
  observer always fires once when observation starts.

## 3. Errors and labels
Nearly every WebGPU object accepts a `label` (`label: 'gbuffer pass'`). Implementations include
the labels of related objects in error messages, so label everything.

## 4. Device loss
```js
device.lost.then(info => { /* log info.reason; reinitialize unless the app destroyed it */ });
```
After loss, rebuild every GPU object from source data.

## Gotchas
- `requestAdapter` can resolve to null on unsupported hardware: always handle it.

## Verify
- [ ] Granted features and limits are logged at startup.
- [ ] Forced device loss (`device.destroy()` in debug) recovers or degrades gracefully.
- [ ] All objects labelled.

## Checked
2026-10-31. Confirmed against WebGPU Fundamentals (adapter, getPreferredCanvasFormat, labels, ResizeObserver clamp to
maxTextureDimension2D, device.lost) and "Limits and Features" (requiredLimits, requiredFeatures, requestDevice rejects
when unmet). Removed unconfirmed: default limit values, canvas format names, alphaMode and sRGB view-format advice,
error-scope code, async pipeline creation, secure-context and browser-difference notes, powerPreference.
Method: documentation only; no commands were run.
