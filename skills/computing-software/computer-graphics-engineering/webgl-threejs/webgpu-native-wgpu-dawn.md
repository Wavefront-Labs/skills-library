---
id: computing-software.computer-graphics-engineering.webgl-threejs.webgpu-native-wgpu-dawn
name: webgpu-native-wgpu-dawn
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, webgpu, wgpu, dawn, webgpu-native, webgpu-h, rust-graphics]
level: advanced
status: docs-checked
description: "Use WebGPU outside the browser with wgpu (Rust, with wgpu-native for C) or Dawn (C++) via webgpu.h: choosing an implementation, backends, and backend selection."
sources: ["https://wgpu.rs/", "https://github.com/gfx-rs/wgpu", "https://dawn.googlesource.com/dawn", "https://github.com/webgpu-native/webgpu-headers", "https://eliemichel.github.io/LearnWebGPU/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native WebGPU: wgpu and Dawn

## 1. Pick an implementation
| | wgpu | Dawn |
|---|---|---|
| Language | Rust; C bindings via wgpu-native | C++ wrapper over `webgpu.h` |
| Used by | Firefox, Servo, Deno | Chromium |
| Backends | Vulkan, Metal, D3D12, OpenGL; WebGL2 and WebGPU on wasm | see the Dawn overview |

- wgpu is a pure-Rust API based on the WebGPU standard. Vulkan, Metal and DX12 are first-class; OpenGL is downlevel/best effort. On the web it runs on WebGPU or WebGL2 via wasm.
- Dawn implements `webgpu.h`, a one-to-one mapping of the WebGPU IDL, and is the underlying implementation of WebGPU in Chromium. It also ships a C++ wrapper for `webgpu.h`.
- To use wgpu from C or other languages, use wgpu-native. Learn WebGPU (for C++) teaches wgpu-native from C++.
- `webgpu.h` (webgpu-native/webgpu-headers) is the shared C header.

## 2. Selecting a wgpu backend
Examples, tests and `::from_env()` methods read environment variables:
- `WGPU_BACKEND`: comma-separated list of backends (vulkan, metal, dx12, gl).
- `WGPU_ADAPTER_NAME`: case-insensitive substring of the adapter name.

API names change between wgpu versions; pin the version and follow the changelog.

## 3. Sharing with web builds
wgpu follows the WebGPU API, so the same WGSL and a very similar API structure carry over between native and the browser (WebGPU Fundamentals is also a useful tutorial for wgpu, minus Rust/JavaScript differences).

## Checked
2026-11-01. Confirmed against wgpu.rs, the gfx-rs/wgpu README (backends, platform support, users, environment variables, wgpu-native), the Dawn overview and the Learn WebGPU site. Removed: Rust code sample, Firefox/Deno/Bevy/Node/Electron beyond what the README states, native-only feature list, downlevel limits, debugging flags, surface and present-mode gotchas, shader front-end claims (naga, Tint).
Method: documentation only; no commands were run.
