---
id: computing-software.software-engineering.tauri.tauri-linux-graphics-debugging
name: tauri-linux-graphics-debugging
category: computing-software
field: software-engineering
product: tauri
tags: [debug-linux-graphics, tauri, webkitgtk, nvidia]
level: practitioner
status: docs-checked
description: "Diagnose blank windows, flicker and resize crashes in Tauri on Linux (WebKitGTK, often NVIDIA) with ordered environment-variable workarounds."
sources:
  - "https://v2.tauri.app/develop/debug/linux-graphics/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux graphics debugging

Goal: fix rendering problems when Tauri (WebKitGTK) and the graphics driver disagree, most often on NVIDIA.

## Symptoms

- Window opens blank or white; flickers, especially on resize.
- App dies on resize with no useful error.
- Console: `AcceleratedSurfaceDMABuf was unable to construct a complete framebuffer`.
- Console: `Gdk-Message: Error 71 (Protocol error) dispatching to Wayland display.`

Most come from the WebKitGTK DMABUF renderer requesting buffer formats the NVIDIA driver does not provide.

## Workarounds, in order

The earlier ones keep hardware acceleration.

1. Ensure kernel mode setting is on. NVIDIA drivers older than 545 often need `nvidia_drm.modeset=1` as a kernel parameter.
2. Set `__NV_DISABLE_EXPLICIT_SYNC=1`. Often fixes the Wayland `Error 71` crash without a performance cost.
3. Set `WEBKIT_DISABLE_DMABUF_RENDERER=1`. Fixes the framebuffer error and `Error 71`, at the cost of the faster rendering path.
4. Set `WEBKIT_DISABLE_COMPOSITING_MODE=1`. Last resort for the silent crash on resize; disables accelerated compositing entirely.

Test by setting them in your shell, or set one in `main()` before the webview is created:

```rust
fn main() {
  #[cfg(target_os = "linux")]
  std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");

  tauri::Builder::default()
    // ...
}
```

Ship an unconditional override only if you have verified your app is affected: it disables a faster path for everyone, including users on working setups.

## Silent WebGL and canvas slowness

- WebGL2 context creation succeeds even when backed by a software rasterizer or slow presentation path; there is no error to catch.
- WebKitGTK masks the renderer string: `WEBGL_debug_renderer_info` reports `Apple GPU` on every Linux machine.

This shows as high input latency or low frame rates in WebGL-heavy views while the same code is fast in a regular browser. Give WebGL paths a non-WebGL fallback on Linux and consider a user setting to switch.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/debug/linux-graphics/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
