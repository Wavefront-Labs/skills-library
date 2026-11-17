---
id: computing-software.software-engineering.wails.manual-build-steps
name: manual-build-steps
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, build, manual-build, upx, winres, ldflags, wails-build]
level: practitioner
status: docs-checked
description: "Reproduce what wails build and wails dev do by hand: frontend install and build, Windows icon and manifest, go build flags, and UPX."
sources: [https://wails.io/docs/guides/manual-builds]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a Wails project without the CLI (e.g. in custom CI), knowing what the CLI does.

Order: install frontend deps, build frontend, generate build assets, compile, optionally compress.

## 1. Install frontend dependencies
CLI: skipped with `-s`; needs a `frontend:install` key in `wails.json` and a `package.json` in the frontend directory. It keeps an MD5 of `package.json` in `package.json.md5` and runs the install only if the sum changed, `node_modules` is missing, or `-f` is given. Manual: `npm install`.

## 2. Build frontend
CLI: skipped with `-s`; runs `frontend:build` in the frontend directory if set. Manual: `npm run build` (or your script).

## 3. Generate assets
CLI: skipped with `-nopackage`. Creates a default `build/appicon.png` if missing. On Windows: creates `build/windows/icon.ico` from the png (sizes 256, 128, 64, 48, 32, 16) with winicon, creates a default `build/windows/<projectname>.manifest` if missing, then uses winres to bundle icon and manifest into a `.syso`.
Manual: make the `.ico` (winicon or other), write/update the `.manifest`, and generate the `.syso` with the winres CLI.

## 4. Compile
CLI defaults:
- `wails dev`: `-tags dev -gcflags "all=-N -l"`
- `wails build`: `-tags desktop,production -ldflags "-w -s"`; on Windows `-ldflags "-w -h -H windowsgui"`
- extra `-tags` and `-ldflags` are appended; `-o` is passed through; `-compiler` picks the Go compiler; `-clean` deletes and recreates `build`.

Manual:
```sh
go build -tags dev -gcflags "all=-N -l"
go build -tags desktop,production -ldflags "-w -s -H windowsgui"
```
Compile in the same directory as the `.syso` file.

## 5. Compress
CLI `-upx` runs `upx` with defaults; `-upxflags` replaces the defaults. Manual: `upx [flags]`.

Related: `computing-software.software-engineering.wails.dev-server-and-frontend-build-hooks`.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Manual Builds" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
