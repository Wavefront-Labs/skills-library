---
id: computing-software.software-engineering.wails.wails-linux-and-debug-options
name: wails-linux-and-debug-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, linux, debug, options]
level: practitioner
status: docs-checked
description: "Set Wails Linux options (window icon, translucency, WebView GPU policy, program name) and the Debug option that opens the inspector on startup."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails Linux and Debug options

Goal: configure `options.App.Linux` (`*linux.Options`) and `options.App.Debug`.

## Linux

```go
Linux: &linux.Options{
    Icon:                icon,
    WindowIsTranslucent: false,
    WebviewGpuPolicy:    linux.WebviewGpuPolicyAlways,
    ProgramName:         "wails",
},
```

- `Icon` (`[]byte`): the window icon, used when minimised (iconified). Pass it at its natural drawn size; scaling is deferred to the end for quality. Some window managers also show it in the frame, others ignore it. GNOME on Wayland does not display it; use a `.desktop` file there. KDE should work.
- `WindowIsTranslucent` (bool): translucent background; some window managers ignore it or give a black window.
- `WebviewGpuPolicy`: default `WebviewGpuPolicyAlways` (hardware acceleration always on); `WebviewGpuPolicyOnDemand` (as requested by web content); `WebviewGpuPolicyNever` (always off).
- `ProgramName` (string): sets the program name via GTK `g_set_prgname()`; do not localise. It helps window grouping and desktop icons when a `.desktop` file's `Name` differs from the executable filename.

## Debug

`Debug: options.Debug{OpenInspectorOnStartup: true}` opens the WebInspector at startup. The docs say this applies to debug builds.

Related: `computing-software.software-engineering.wails.wails-assetserver-options` for the WebKit2GTK build tags.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), focusing on the Linux subsection (Icon, WindowIsTranslucent, WebviewGpuPolicy and its value table, ProgramName) and the Debug subsection (OpenInspectorOnStartup, described on the page as applying to debug builds). The GNOME-on-Wayland and KDE icon notes and the g_set_prgname wording matched. No claims were trimmed.

Method: documentation only; no commands were run.
