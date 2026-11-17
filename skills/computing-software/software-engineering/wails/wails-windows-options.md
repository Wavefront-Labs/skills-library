---
id: computing-software.software-engineering.wails.wails-windows-options
name: wails-windows-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, windows, webview2, theme, options]
level: practitioner
status: docs-checked
description: "Configure options.App.Windows in Wails: translucency and backdrop, themes and custom title-bar colours, WebView2 paths, zoom, GPU, suspend and resume hooks."
sources: [https://wails.io/docs/reference/options, https://github.com/wailsapp/wails/blob/master/v2/pkg/options/windows/windows.go]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails Windows options

Goal: tune `options.App.Windows` (`*windows.Options`, package `github.com/wailsapp/wails/v2/pkg/options/windows`).

## Transparency and backdrop

- `WebviewIsTransparent`: with `rgba(0,0,0,0)` CSS background the host window shows through; often paired with `WindowIsTranslucent`.
- `WindowIsTranslucent`: translucent window background. Before Windows 11 build 22621 it uses BlurBehind (can be slow); after, faster newer types.
- `BackdropType` (needs build 22621+, only when translucent): `windows.Auto`, `None`, `Acrylic`, `Mica`, `Tabbed`.
- `ContentProtection`: blocks capture by other apps (SetWindowDisplayAffinity with `WDA_EXCLUDEFROMCAPTURE`; older Windows than 10 2004 uses `WDA_MONITOR`, capturing black).

## Theme

`Theme` (Windows 10 2004/20H1+): `windows.SystemDefault` (default, follows system), `windows.Dark`, `windows.Light`.

`CustomTheme` (`*windows.ThemeSettings`, Windows 10/11 build 22000+) sets title bar, title text and border colours for light/dark, active and inactive (fields like `DarkModeTitleBar`, `DarkModeTitleBarInactive`, `LightModeBorder`...). Values are `int32` in `0x00BBGGAA`; build them with `windows.RGB(r, g, b uint8)`. Unset values default to black.

```go
CustomTheme: &windows.ThemeSettings{
    DarkModeTitleBar:  windows.RGB(255, 0, 0),
    DarkModeTitleText: windows.RGB(0, 255, 0),
    DarkModeBorder:    windows.RGB(0, 0, 255),
    DarkModeTitleBarInactive: windows.RGB(128, 0, 0),
},
```

## WebView2 and window behaviour

- `WebviewUserDataPath`: where WebView2 stores user data; empty means `%APPDATA%\[BinaryName.exe]`.
- `WebviewBrowserPath`: directory of a fixed-version WebView2 runtime; empty uses the system install. The path must not contain `\Edge\Application\`.
- `ZoomFactor` (float64): the WebView2 zoom factor (matches Edge user zoom). `IsZoomControlEnabled` (bool): lets the user change it; the factor can still be set in options while the user is blocked from changing it (for example a kiosk).
- `DisablePinchZoom`, `EnableSwipeGestures`, `DisableWindowIcon` (hides top-left title bar icon), `DisableFramelessWindowDecorations` (drops Aero shadow and Windows 11 rounded corners in frameless mode).
- `WebviewGpuIsDisabled` (bool): disable GPU hardware acceleration for the webview.
- `WindowClassName`: window class, `wailsWindow` if empty.
- `ResizeDebounceMS` (uint16): debounce redraws while resizing; 0 redraws as fast as possible.
- `Messages` (`*windows.Messages`): strings shown by the WebView2 installer when no runtime is found; localise as needed.
- `OnSuspend` / `OnResume` (`func()`): called when Windows enters and leaves low power mode.

## Gaps

The options page's overview example spells the GPU field `WebviewGpuDisabled`, but its detail section and the Go struct (`v2/pkg/options/windows/windows.go`) both name it `WebviewGpuIsDisabled`; use that.

## Checked

2026-11-07. Read the whole Options reference page (wails.io/docs/reference/options, source file website/docs/reference/options.mdx from the wailsapp/wails repo), including the Go example block, the "Windows" subsection (WebviewIsTransparent through WindowClassName), the BackdropType, Theme and CustomTheme tables and the ThemeSettings struct; no embedded include files exist on that page. Confirmed: BlurBehind before build 22621, BackdropType values and the 22621 requirement, WDA_EXCLUDEFROMCAPTURE / WDA_MONITOR behaviour, Theme minimum (Windows 10 2004/20H1), CustomTheme minimum (build 22000), the 0x00BBGGAA format and black default, WebView2 path defaults and the Edge path warning, ResizeDebounceMS, OnSuspend/OnResume. Trimmed: ZoomFactor "initial zoom" (page says zoom factor, matching Edge zoom). The WebviewGpuIsDisabled spelling was confirmed against the Go source file windows.go (added to sources, read for the GPU, ResizeDebounceMS, EnableSwipeGestures and WindowClassName fields only); the unfinished "check the Go package" note was replaced with the result.

Method: documentation only; no commands were run.
