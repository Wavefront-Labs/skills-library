---
id: computing-software.software-engineering.wails.troubleshooting-runtime-and-display
name: troubleshooting-runtime-and-display
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, troubleshooting, runtime, macos, windows, webview, variadic]
level: practitioner
status: docs-checked
description: "Fix Wails runtime and display issues: blank window, invalid Mac app, stale Windows icon, variadic method calls, lost runtime after navigation, macOS white flash."
sources: [https://wails.io/docs/guides/troubleshooting]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting a running Wails app

- **White/blank screen.** Check the embed in `main.go` (`//go:embed all:frontend/dist` then `var assets embed.FS`) and that `frontend/dist` actually holds your assets. On Mac also try adding to `Info.plist`:
  ```xml
  <key>NSAppTransportSecurity</key>
  <dict><key>NSAllowsLocalNetworking</key><true/></dict>
  ```
- **Mac app shows as invalid in Finder.** Likely a bad `info.plist` (e.g. wrong binary name). Edit `build/<yourapp>.app/Contents/info.plist` to test, then copy the fix back to `build/darwin` so it persists.
- **Wrong icon in Windows Explorer.** Delete the hidden `IconCache.db` in `the user AppData Local folder` to force a rebuild of the icon cache.
- **Variadic backend methods.** `func (a *App) TestFunc(msg string, args ...interface{}) error` fails when called with spread args from JS. Pass the array as one argument instead: `window.go.main.App.TestFunc(msg, args)` (not `...args`).
- **Cannot call Go after navigating away from `index.html`.** The runtime context is lost on a new HTML page. Add to the new page's `<head>`:
  ```html
  <script src="/wails/ipc.js"></script>
  <script src="/wails/runtime.js"></script>
  ```
- **Mac window flashes white at startup.** The webview default background is white. Make it transparent so the window background shows:
  ```go
  Mac: &mac.Options{ WebviewIsTransparent: true },
  ```
- **WebView2 reports "ProcessFailed ... kind" on Windows.** The page only points you to Microsoft's CoreWebView2ProcessFailedKind documentation to interpret it.
- **`wails doctor` says WebView2 is missing though installed.** Likely the runtime is for a different architecture; download the matching one from Microsoft's WebView2 page.

Build and install problems: `computing-software.software-engineering.wails.troubleshooting-dev-and-build`.

## Checked

2026-11-07. Read the whole Troubleshooting guide (website/docs/guides/troubleshooting.mdx). Compared against these sections: white/blank screen (embed line, NSAllowsLocalNetworking plist snippet), Mac application not valid (info.plist path, copy back to build/darwin), wrong icon in Windows Explorer (IconCache.db), variadic arguments workaround, navigating away from index.html (the two script tags), Mac white flash (WebviewIsTransparent), WebView2 process-failed kind and the wails doctor architecture mismatch. The referenced GitHub issues were not opened; the page screenshot of the invalid Mac app was not viewed. No claims were trimmed.

Method: documentation only; no commands were run.
