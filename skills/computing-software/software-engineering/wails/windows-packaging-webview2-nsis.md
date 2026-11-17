---
id: computing-software.software-engineering.wails.windows-packaging-webview2-nsis
name: windows-packaging-webview2-nsis
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, windows, webview2, nsis, installer, packaging]
level: practitioner
status: docs-checked
description: "Package a Wails app for Windows: choose the -webview2 runtime strategy or a fixed runtime, build an NSIS installer with -nsis, and hide windows of spawned processes."
sources: [https://wails.io/docs/guides/windows, https://wails.io/docs/guides/windows-installer]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows packaging: WebView2 runtime and NSIS installer

Goal: make the app run on machines without WebView2 and ship an installer.

## WebView2 strategy (`wails build -webview2 <mode>`)

Windows 11 ships the runtime; some machines lack it (or have one too old). Modes:
- Download: prompts the user, then downloads and runs Microsoft's bootstrapper.
- Embed: bundles the bootstrapper in the app (about 150k larger) and offers to run it.
- Browser: prompts, opens the official WebView2 page, then exits and leaves installation to the user.
- Error: shows an error and does nothing else.

## Fixed-version runtime

Download the fixed version runtime from Microsoft and bundle it or fetch it with your app, then point Wails at it:
```go
Windows: &windows.Options{ WebviewBrowserPath: "" } // set to the runtime folder
```
With `WebviewBrowserPath` set, the error strategy is forced on version mismatch or an invalid path. The download is a `.cab`; extract with `expand {path to the package} -F:* {destination folder}`.

## NSIS installer

Install NSIS: `scoop bucket add extras` then `scoop install nsis`; or `winget install NSIS.NSIS --silent`; or `choco install nsis`; Linux via the `nsis` package; macOS `brew install nsis`. A manual install needs the folder with `makensis.exe` (Bin) on PATH. New projects get config in `build/windows/installer`, read from `installer/info.json`, which uses the `Info` section of `wails.json` (companyName, productName, productVersion, copyright, comments). Build:
```
wails build -nsis
```
The installer lands in `build/bin`.

## Hiding windows of spawned programs

```go
cmd := exec.Command("your_script.exe")
cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true, CreationFlags: 0x08000000}
cmd.Start()
```

## Checked

2026-11-07. Read the whole Windows guide (website/docs/guides/windows.mdx: the four -webview2 modes, the ~150k embed overhead, fixed-version runtime and forced error strategy, the .cab expand command, hiding spawned windows) and the whole NSIS installer guide (website/docs/guides/windows-installer.mdx: scoop, winget, choco, Linux nsis package, brew, makensis.exe Bin on PATH, build/windows/installer, installer/info.json and the Info section keys, wails build -nsis, output in build/bin). The Microsoft distribution page linked for the fixed runtime was not opened. No claims were trimmed.

Method: documentation only; no commands were run.
