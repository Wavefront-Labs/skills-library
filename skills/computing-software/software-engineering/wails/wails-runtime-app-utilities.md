---
id: computing-software.software-engineering.wails.wails-runtime-app-utilities
name: wails-runtime-app-utilities
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, clipboard, browser]
level: practitioner
status: docs-checked
description: "Use Wails runtime helpers: Hide, Show, Quit, Environment, ResetSignalHandlers on Linux, text clipboard access and BrowserOpenURL."
sources: [https://wails.io/docs/reference/runtime/intro, https://wails.io/docs/reference/runtime/clipboard, https://wails.io/docs/reference/runtime/browser]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime app utilities

Goal: use the general-purpose runtime functions. Go package: `github.com/wailsapp/wails/v2/pkg/runtime`; every Go call takes `ctx` (from OnStartup or, safer, OnDomReady). The JS runtime lives on `window.runtime`, with TypeScript declarations generated into `wailsjs` in dev mode.

## App control

- `Hide(ctx)` / `Show(ctx)` / JS `Hide()` `Show()`: on Mac `Hide` hides the whole application like the standard Hide menu item and `Show` brings the application back to the foreground; on Windows and Linux it equals `WindowHide` / `WindowShow`.
- `Quit(ctx)` / `Quit()`.
- `Environment(ctx) EnvironmentInfo` / JS `Environment(): Promise<EnvironmentInfo>` with `BuildType`, `Platform`, `Arch` (TS lowercase: `buildType`, `platform`, `arch`).

## ResetSignalHandlers (Go, Linux only)

On Linux, WebKit may install signal handlers without `SA_ONSTACK`, so Go cannot recover from nil dereference or other memory faults. `runtime.ResetSignalHandlers()` restores them; it is a no-op on macOS and Windows. Call it in each goroutine, immediately before the code that might panic, because WebKit may reset handlers at any time:

```go
go func() {
    defer func() {
        if err := recover(); err != nil {
            log.Printf("Recovered from panic: %v", err)
        }
    }()
    runtime.ResetSignalHandlers()
    // code that might panic
}()
```

## Clipboard (text only)

- `ClipboardGetText(ctx) (string, error)` / JS `ClipboardGetText(): Promise<string>`; empty clipboard gives an empty string.
- `ClipboardSetText(ctx, text) error` / JS `ClipboardSetText(text): Promise<boolean>` (true on success).

## Browser

`BrowserOpenURL(ctx, url)` / JS `BrowserOpenURL(url)` opens a URL in the system browser.

Related: `computing-software.software-engineering.wails.wails-runtime-window-control`.

## Checked

2026-11-07. Read the whole runtime intro page (website/docs/reference/runtime/intro.mdx: Hide, Show, Quit, Environment/EnvironmentInfo, ResetSignalHandlers with its Linux-only info box, example and per-goroutine warning), the whole Clipboard page (text only, empty string, Promise<boolean> result) and the whole Browser page (BrowserOpenURL). Trimmed: the Mac Show wording now matches the page (brings the app back to the foreground). The wailsjs TypeScript declarations statement matched the intro text.

Method: documentation only; no commands were run.
