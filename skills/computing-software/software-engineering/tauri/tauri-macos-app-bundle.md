---
id: computing-software.software-engineering.tauri.tauri-macos-app-bundle
name: tauri-macos-app-bundle
category: computing-software
field: software-engineering
product: tauri
tags: [macos-app-bundle, tauri, info-plist]
level: practitioner
status: docs-checked
description: "Package a Tauri app as a macOS .app bundle and configure Info.plist, localization, entitlements, minimum version, frameworks and extra files."
sources:
  - "https://v2.tauri.app/distribute/macos-application-bundle/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri macOS application bundle

Goal: produce and configure the `.app` directory, which holds the executable, resources, `Info.plist` and frameworks. Build on a Mac with `tauri build --bundles app`.

## Layout

`<productName>.app/Contents` contains `Info.plist` and extra files from `bundle > macOS > files`; `MacOS` holds the executable; `Resources` holds `icon.icns` and `bundle > resources`; also `_CodeSignature`, `Frameworks`, `PlugIns`, `SharedSupport`.

## Info.plist

Tauri sets the binary name, version, bundle identifier, minimum system version and more. To extend, create `src-tauri/Info.plist` with extra keys such as `NSCameraUsageDescription` and `NSMicrophoneUsageDescription`; it is merged with generated values (overriding defaults like version can conflict).

Localization: add `InfoPlist.strings` files in `<lang-code>.lproj` directories (for example `src-tauri/infoplist/de.lproj/InfoPlist.strings`, with `Key = "text";` lines) and bundle them:

```json
{ "bundle": { "resources": { "infoplist/**": "./" } } }
```

## Entitlements

Create `src-tauri/Entitlements.plist` (for example `com.apple.security.app-sandbox` set to `<true/>`) and set `bundle > macOS > entitlements` to `"./Entitlements.plist"`. They apply when the app is signed.

## Other options

- `bundle > macOS > minimumSystemVersion`: default is macOS 10.13 and above; for example `"12.0"`.
- `bundle > macOS > frameworks`: system frameworks by name without `.framework` (from `$HOME/Library/Frameworks`, `/Library/Frameworks/`, `/Network/Library/Frameworks/`); local frameworks and dylibs by path relative to `src-tauri`.
- `bundle > macOS > files`: maps destination (under `Contents`) to source relative to `tauri.conf.json`, for example `"embedded.provisionprofile": "./profile-name.provisionprofile"` and `"SharedSupport/docs.md": "./docs/index.md"`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/macos-application-bundle/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
