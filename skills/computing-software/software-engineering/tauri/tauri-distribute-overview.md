---
id: computing-software.software-engineering.tauri.tauri-distribute-overview
name: tauri-distribute-overview
category: computing-software
field: software-engineering
product: tauri
tags: [distribute-overview, tauri, distribution]
level: intro
status: docs-checked
description: "Build, bundle, version and sign a Tauri app, and pick the distribution format for Linux, macOS, Windows, Android and iOS."
sources:
  - "https://v2.tauri.app/distribute/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri distribution overview

Goal: turn a Tauri app into platform bundles or store uploads.

## Build

The CLI builds via `build`, `android build` and `ios build`. For example `npm run tauri build` or `cargo tauri build`. By default `build` also bundles for the configured formats.

To customise bundling, split the steps:

```sh
tauri build --no-bundle
# bundle for distribution outside the macOS App Store
tauri bundle --bundles app,dmg
# bundle for App Store distribution
tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

(Prefix with your runner, e.g. `npm run tauri` or `cargo tauri`.)

## Versioning

Set `tauri.conf.json > version` (recommended). If unset, Tauri uses `package > version` from `src-tauri/Cargo.toml`. Some platforms have limits on the version string; see each platform page.

## Signing

Code signing applies a digital signature to executables and bundles, validating the provider's identity. It is required on most platforms; guides exist for macOS, Windows, Linux, Android and iOS.

## Choosing a format

- Linux: Debian package, Snap, AppImage, Flatpak, RPM or Arch User Repository (AUR).
- macOS: App Store or a DMG installer as direct download. Both need code signing; distributing outside the App Store also needs notarization.
- Windows: Microsoft Store or a Windows installer.
- Android: Google Play.
- iOS: App Store.
- Cloud services: CrabNebula Cloud, which distributes globally and supports auto updates out of the box.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/ (page text including code blocks and tabs read in full).
Removed: the sentence calling App Bundle the base format (not on the page).
Method: documentation only; no commands were run.
