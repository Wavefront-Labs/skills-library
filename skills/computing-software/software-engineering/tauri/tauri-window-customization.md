---
id: computing-software.software-engineering.tauri.tauri-window-customization
name: tauri-window-customization
category: computing-software
field: software-engineering
product: tauri
tags: [window-customization, tauri, titlebar, windows]
level: practitioner
status: docs-checked
description: "Build a custom Tauri titlebar with decorations off, window permissions, a drag region and JavaScript buttons, or use a transparent titlebar on macOS."
sources:
  - "https://v2.tauri.app/learn/window-customization/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri window customization

Goal: change the look of the app window, such as a custom titlebar. Window settings can be changed in `tauri.conf.json`, through the JavaScript window API, or through the Window in Rust.

## Custom titlebar

1. Set `decorations` to `false` on the window in `tauri.conf.json`.
2. Plugin commands are blocked by default, so add permissions to a capability file:

```json
"permissions": [
  "core:window:default",
  "core:window:allow-close",
  "core:window:allow-minimize",
  "core:window:allow-toggle-maximize",
  "core:window:allow-start-dragging"
]
```

3. Add a titlebar element at the top of `<body>`, with `data-tauri-drag-region` on the draggable div and buttons with ids `titlebar-minimize`, `titlebar-maximize` and `titlebar-close`. Style it (for example `position: fixed; top: 0; left: 0; right: 0; height: 30px; user-select: none`) and move other content down.
4. Wire the buttons:

```javascript
import { getCurrentWindow } from '@tauri-apps/api/window';
// with "withGlobalTauri": true use window.__TAURI__.window
const appWindow = getCurrentWindow();

document.getElementById('titlebar-minimize')?.addEventListener('click', () => appWindow.minimize());
document.getElementById('titlebar-maximize')?.addEventListener('click', () => appWindow.toggleMaximize());
document.getElementById('titlebar-close')?.addEventListener('click', () => appWindow.close());
```

`data-tauri-drag-region` only works on the element it is applied to, not its children, so buttons and inputs keep working. On Windows, `*[data-tauri-drag-region] { app-region: drag; }` makes a plain title bar work with touch and pen.

For custom drag behavior, drop the attribute and handle `mousedown` yourself: when `e.buttons === 1`, call `appWindow.toggleMaximize()` if `e.detail === 2`, else `appWindow.startDragging()`.

## macOS: transparent titlebar

A custom titlebar loses system features on macOS such as window moving and aligning. Alternative: remove the main window from `tauri.conf.json`, create it in `setup` with `WebviewWindowBuilder`, apply `.title_bar_style(TitleBarStyle::Transparent)` under `#[cfg(target_os = "macos")]`, then set the background colour via the `objc2-app-kit` crate (features `NSColor`, `NSWindow`, `objc2-core-foundation`) with `ns_window.setBackgroundColor(Some(&bg_color))`.

## Checked

Checked 2026-11-08 against the Tauri v2 window customization page: decorations, the five core:window permissions, data-tauri-drag-region behaviour, button ids, JavaScript window API, app-region tip for Windows, manual mousedown dragging and the macOS transparent titlebar steps including the objc2-app-kit features. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
