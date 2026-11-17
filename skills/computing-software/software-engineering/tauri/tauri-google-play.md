---
id: computing-software.software-engineering.tauri.tauri-google-play
name: tauri-google-play
category: computing-software
field: software-engineering
product: tauri
tags: [google-play, tauri, android-bundle]
level: practitioner
status: docs-checked
description: "Build a signed Tauri Android AAB or APK for Google Play: icons, version code, architectures, min SDK and the first manual upload."
sources:
  - "https://v2.tauri.app/distribute/google-play/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Google Play distribution

Tauri uses an Android Studio project, so official Android publishing practice also applies. You need a Play Console developer account and Android code signing set up.

## Icon

After `tauri android init`, run `tauri icon /path/to/app-icon.png`.

## Build

```sh
tauri android build --aab                 # Android App Bundle for upload (recommended)
tauri android build --apk                 # APKs for testing or outside the store
tauri android build --aab --target aarch64 --target armv7
tauri android build --apk --split-per-abi
```

By default all architectures are built (aarch64, armv7, i686, x86_64) and the AAB or APK is universal. `--split-per-abi` makes one bundle per target; it is only useful for testing or distribution outside Google Play, which handles architectures for you.

## Version code

Tauri derives it from `version`: `versionCode = major*1000000 + minor*1000 + patch`. Override with `bundle > android > versionCode`, for example `100` for sequential codes.

## Minimum Android version

Tauri apps support Android 7.0 (Nougat, SDK 24) and up. Raise it with `bundle > android > minSdkVersion`, for example `28`.

## Upload

The AAB is at `gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab`. Create a release and upload it in the Play Console. The first upload must be made manually on the website so it can verify the app signature and bundle identifier. Tauri cannot yet automate release creation (that would use the Google Play Developer API); it is a work in progress.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/google-play/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
