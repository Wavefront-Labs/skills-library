---
id: computing-software.software-engineering.wails.troubleshooting-dev-and-build
name: troubleshooting-dev-and-build
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, troubleshooting, build, macos, proxy, typescript, bindings]
level: practitioner
status: docs-checked
description: "Fix Wails install and build problems: missing wails command, Go proxy blocked, macOS toolchain and linker errors, too many open files, esbuild host mismatch, stuck bindings."
sources: [https://wails.io/docs/guides/troubleshooting]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting installs, dev and builds

Goal: match a symptom to the fix the Wails troubleshooting guide gives.

- **`wails` command missing.** Usually `go/bin` in your home directory is not on `PATH`. Fix the Go install per the guide, then close and reopen terminals so the environment change applies.
- **Proxy errors installing Wails** (dial tcp timeouts to proxy.golang.org, reported from China): set the proxy manually.
  ```
  go env -w GO111MODULE=on
  go env -w GOPROXY=https://goproxy.cn,direct
  ```
- **Generated TypeScript has wrong types.** Specify types with the `ts_type` struct tag (see typescriptify-golang-structs "custom types").
- **`too many open files` on macOS during `wails dev`.** The default limit is 256; run `ulimit -n 1024`. (FSNotify may move to fsevents; tracked in wails issue 1733.)
- **Weird macOS compile errors** (e.g. "function does not return NSString" from Foundation headers). Normally an OS / Xcode Command Line Tools version mismatch: upgrade the tools. If it persists, check `xcode-select -p`; if it prints `/Applications/Xcode.app/Contents/Developer`, run `sudo xcode-select --switch /Library/Developer/CommandLineTools`.
- **macOS link error `_OBJC_CLASS_$_UTType` undefined.** Ensure the latest SDK; otherwise:
  ```shell
  export CGO_LDFLAGS="-framework UniformTypeIdentifiers" && go build -tags dev -gcflags "all=-N -l"
  ```
- **Cannot start service: Host version does not match binary version.** Add `frontend/node_modules` and `frontend/package-lock.json` to `.gitignore`. If it happens, delete both and rerun `wails build` or `wails dev`.
- **Build stuck on "Generating bindings".** Bindings generation runs your app in a special mode; an endless loop or an app that does not exit after `wails.Run()` finishes hangs it. Make sure your code exits.

Runtime and display problems are in `computing-software.software-engineering.wails.troubleshooting-runtime-and-display`; Windows admin/WebView2 in `computing-software.software-engineering.wails.windows-webview2-admin-data-dir`.

## Checked

2026-11-07. Read the whole Troubleshooting guide (website/docs/guides/troubleshooting.mdx). Compared against these sections: missing wails command, Go proxy errors (goproxy.cn commands), wrong generated TypeScript (ts_type tag), too many open files on Mac (256 limit, ulimit -n 1024, issue 1733), weird Mac compilation errors (Command Line Tools, xcode-select -p and --switch), the UTType linker error with CGO_LDFLAGS, "Host version does not match binary version" (.gitignore advice and delete-and-rerun fix) and the stuck "Generating bindings" build. The linked GitHub issues and the typescriptify-golang-structs README were not opened. No claims were trimmed.

Method: documentation only; no commands were run.
