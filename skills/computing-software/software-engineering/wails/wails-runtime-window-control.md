---
id: computing-software.software-engineering.wails.wails-runtime-window-control
name: wails-runtime-window-control
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, window, screen]
level: practitioner
status: docs-checked
description: "Control the Wails window from Go or JS runtime: title, size, position, fullscreen, maximise, minimise, theme, background colour, print, ExecJS and screens."
sources: [https://wails.io/docs/reference/runtime/window, https://wails.io/docs/reference/runtime/screen]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime window control

Goal: change the window at runtime. Go calls take `ctx` first (from OnStartup/OnDomReady); JS calls omit it.

## Calls (Go / JS)

- Title: `WindowSetTitle(ctx, title)`.
- Fullscreen: `WindowFullscreen`, `WindowUnfullscreen` (restores prior size and position), `WindowIsFullscreen` (JS returns Promise<boolean>).
- Position: `WindowCenter` (on the current monitor), `WindowSetPosition(ctx, x, y)` and `WindowGetPosition` (relative to the current monitor; JS returns `Promise<Position>` with x, y).
- Size: `WindowSetSize(ctx, w, h)`, `WindowGetSize`; JS returns `Promise<Size>` with fields `w` and `h`. `WindowSetMinSize` / `WindowSetMaxSize` resize the window if it violates the limit; `0,0` disables the constraint.
- State: `WindowMaximise`, `WindowUnmaximise`, `WindowToggleMaximise`, `WindowIsMaximised`, `WindowMinimise`, `WindowUnminimise`, `WindowIsMinimised`, `WindowIsNormal` (not minimised, maximised or fullscreen), `WindowShow`, `WindowHide`, `WindowSetAlwaysOnTop(ctx, bool)`.
- Reload: `WindowReload` (current page), `WindowReloadApp` (the frontend).
- Theme (Windows only): `WindowSetSystemDefaultTheme`, `WindowSetLightTheme`, `WindowSetDarkTheme`.
- `WindowSetBackgroundColour(ctx, R, G, B, A uint8)`: 0-255 each, shows through transparent pixels. On Windows only alpha 0 or 255 is supported (any non-zero counts as 255).
- `WindowPrint`: opens the native print dialog.
- `WindowExecJS(ctx, js)` (Go only): runs JS asynchronously and returns immediately; errors appear only in the browser console.

## Screens

`ScreenGetAll(ctx) []screen` / JS `ScreenGetAll()` lists connected screens. Fields: `IsCurrent`, `IsPrimary`, `Width`, `Height` (TS: `isCurrent`, `isPrimary`, `width`, `height`).

## Related

Startup values for the same properties: `computing-software.software-engineering.wails.wails-window-startup-options`.

## Checked

2026-11-07. Read the whole Window runtime page (website/docs/reference/runtime/window.mdx: every Window* entry with Go and JS signatures, the 0,0 min/max note, the Windows alpha 0/255 note, Windows-only theme calls, WindowExecJS asynchronous/console-only errors, and the Position and Size TypeScript interfaces) and the whole Screen runtime page (website/docs/reference/runtime/screen.mdx: ScreenGetAll, Screen struct and interface). Every call, return shape and platform note in the skill matched. No claims were trimmed.

Method: documentation only; no commands were run.
