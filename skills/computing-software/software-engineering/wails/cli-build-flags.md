---
id: computing-software.software-engineering.wails.cli-build-flags
name: cli-build-flags
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, cli, build, cross-compile]
level: practitioner
status: docs-checked
description: "Choose wails build flags: platform targets, debug and devtools, obfuscation, UPX, NSIS, webview2 strategy, tags, ldflags and skipping steps."
sources: [https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails build flags

Goal: pick the right flags for a production build. Example: `wails build -clean -o myproject.exe`.

## Method

Output and cleanup: `-clean` (empty build/bin), `-o filename`, `-nopackage`, `-dryrun` (print the build command only).
Targets: `-platform` comma-separated, e.g. `windows/arm64`; without an architecture, `runtime.GOARCH` is used. Defaults come from `GOOS`/`GOARCH` env vars, else the host. Platforms: darwin, darwin/amd64, darwin/arm64, darwin/universal, windows, windows/amd64, windows/arm64, linux, linux/amd64, linux/arm64.
Diagnostics: `-debug` (keeps debug info, debug console, devtools), `-devtools` (devtools in production; Ctrl/Cmd+Shift+F12; will FAIL Mac App Store guidelines), `-race`, `-v 0|1|2`, `-nocolour`.
Compiler: `-compiler`, `-tags "a b"` (quoted; space or comma, not both), `-ldflags`, `-trimpath`.
Speed/skip: `-s` skip frontend, `-skipbindings`, `-skipembedcreate`, `-m` skip mod tidy, `-nosyncgomod`, `-u` update go.mod to the CLI Wails version, `-f` force.
Size/protection: `-upx`, `-upxflags`, `-obfuscated` (garble), `-garbleargs` (default `-literals -tiny -seed=random`).
Windows: `-nsis` installer, `-webview2 download|embed|browser|error` (default download; detail in the Windows guide), `-windowsconsole`.

## Gotchas
- UPX has issues on Apple Silicon and some antivirus products flag UPX-compressed binaries.
- Override the minimum macOS version via env vars: `CGO_CFLAGS=-mmacosx-version-min=10.15.0 CGO_LDFLAGS=-mmacosx-version-min=10.15.0 wails build`.

## Related skills
- computing-software.software-engineering.wails.build-production-binary

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: CLI reference (reference/cli).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
