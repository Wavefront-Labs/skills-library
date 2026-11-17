---
id: computing-software.software-engineering.tauri.tauri-app-icons
name: tauri-app-icons
category: computing-software
field: software-engineering
product: tauri
tags: [app-icons, tauri]
level: intro
status: docs-checked
description: "Generate Tauri app icons for all platforms with the tauri icon command, configure bundle.icon, or create icons manually to the stated sizes."
sources:
  - "https://v2.tauri.app/develop/icons/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri app icons

Goal: replace the default Tauri iconset with your own before shipping.

## Generate

Run `npm run tauri icon` (or `yarn tauri icon`, `pnpm tauri icon`, `cargo tauri icon`, `deno task tauri icon`). Usage: `tauri icon [OPTIONS] [INPUT]`.

- `[INPUT]`: source icon, a squared PNG or SVG with transparency; default `./app-icon.png`.
- `-o, --output <OUTPUT>`: output directory; default is the `icons` directory next to `tauri.conf.json`.
- `-p, --png <PNG>`: custom PNG sizes to generate; the default icons are then not generated.
- `--ios-color <IOS_COLOR>`: iOS icon background color, a CSS Color Module Level 4 string; default `#fff`.

Desktop icons go to `src-tauri/icons` and are bundled automatically. To use another location edit `bundle.icon` in `tauri.conf.json`, for example `["icons/32x32.png", "icons/128x128.png", "icons/128x128@2x.png", "icons/icon.icns", "icons/icon.ico"]`. Mobile icons are placed directly into the Xcode and Android Studio projects.

File types: `icon.icns` is macOS, `icon.ico` is Windows, `*.png` is Linux; `Square*Logo.png` and `StoreLogo.png` are currently unused (intended for AppX/MS Store). Include all icons even if you target only some platforms.

## Manual requirements

- `icon.ico`: layers for 16, 24, 32, 48, 64 and 256 pixels; the 32px layer first for best display in development.
- `png`: width equals height, RGBA, 32 bits per pixel. Desktop sizes commonly 32, 128, 256 and 512; at least match `32x32.png`, `128x128.png`, `128x128@2x.png`, `icon.png`.
- Android: PNGs under `src-tauri/gen/android/app/src/main/res/mipmap-*`, for example `mipmap-mdpi` `ic_launcher.png` and `ic_launcher_round.png` at 48x48 and `ic_launcher_foreground.png` at 108x108; `mipmap-xxxhdpi` is 192x192 and 432x432.
- iOS: PNGs without transparency in `src-tauri/gen/apple/Assets.xcassets/AppIcon.appiconset/`, named `AppIcon-{size}x{size}@{scaling}{extra}.png`, for sizes 20, 29, 40 (1x, 2x, 3x, with an extra icon), 60 (2x, 3x), 76 (1x, 2x), 83.5 (2x) and 512 (2x as `AppIcon-512@2x.png`).

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/icons/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
