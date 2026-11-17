---
id: computing-software.software-engineering.tauri.tauri-development-workflow
name: tauri-development-workflow
category: computing-software
field: software-engineering
product: tauri
tags: [develop-workflow, tauri]
level: practitioner
status: docs-checked
description: "Run tauri dev on desktop and tauri android/ios dev on mobile, set the dev server, open the web inspector and ignore files with .taurignore."
sources:
  - "https://v2.tauri.app/develop/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri development workflow

Goal: run and debug your app during development.

## Dev server

In `tauri.conf.json > build`, set `devUrl` (for example `http://localhost:3000`) and `beforeDevCommand` (for example `npm run dev`). Without a UI framework or bundler, set `frontendDist` to `./src` and the CLI starts a server for you; that folder must contain `index.html`. The built-in server has no mutual authentication or encryption, so never use it on untrusted networks.

## Desktop

Run `npm run tauri dev` (or `yarn tauri dev`, `pnpm tauri dev`, `deno task tauri dev`, `bun tauri dev`, `cargo tauri dev`). The first run can take several minutes. Open the Web Inspector by right-clicking the webview and choosing Inspect, or with `Ctrl + Shift + I` (Windows, Linux) / `Cmd + Option + I` (macOS).

## Mobile

Run `tauri android dev` or `tauri ios dev`. By default it runs on a connected device, otherwise prompts for a simulator; pass a name to choose, for example `tauri ios dev 'iPhone 15'`. Use `--open` to open Xcode or Android Studio; the CLI process must keep running while the IDE is open.

For a physical iOS device the dev server must listen on `TAURI_DEV_HOST`: in Vite use `host: host || false` and `hmr: host ? { protocol: 'ws', host, port: 1421 } : undefined`. Add `--host` to the dev command. To use the device address, open Xcode first and run `tauri ios dev --force-ip-prompt` to select the IPv6 address ending in `::2`.

Inspecting: iOS uses Safari (enable developer features; on a physical device enable Web Inspector in Settings > Safari > Advanced). Android uses `chrome://inspect` in Chrome; physical devices need Developer Options and USB Debugging.

## Rebuilds and source control

`tauri dev` watches `src-tauri` and workspace dependent crates and rebuilds on change; `--no-watch` disables this. Add `.taurignore` files (gitignore syntax, for example `build/`, `src/generated/*.rs`) in `src-tauri` or the workspace root. Commit `src-tauri/Cargo.lock`; do not commit `src-tauri/target`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
