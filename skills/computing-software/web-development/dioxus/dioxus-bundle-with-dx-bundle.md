---
id: computing-software.web-development.dioxus.dioxus-bundle-with-dx-bundle
name: dioxus-bundle-with-dx-bundle
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dx-bundle, package-types, json-output, dx-serve-ios, dx-serve-android, ip-port, dioxus-toml]
level: practitioner
status: docs-checked
description: "Test on iOS/Android/desktop and bundle Dioxus apps with dx bundle: --web output layout, IP and PORT env vars, --package-types, Dioxus.toml bundle section, --json-output with jq."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/bundle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test on devices and bundle with dx bundle

## Run on other platforms
```sh
dx serve --ios       # iOS Simulator
dx serve --android   # Android emulator
dx serve --desktop   # macOS, Windows, Linux
```
iOS needs a macOS machine, Xcode, an iOS SDK/emulator pack and the rustup targets `aarch64-apple-ios aarch64-apple-ios-sim`; this requires an Apple Developer account, with no fees needed until you sign the app (signing is required for the App Store and for testing on a device). Android needs the NDK and SDK, JAVA_HOME / ANDROID_HOME / NDK_HOME set, the `emulator` tool on PATH, an emulator, and the targets `aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android`. If Android setup fails, enable dx verbose mode.

## Web bundle
```sh
dx bundle --web
```
Prints the path of the generated `public` folder. Next to `public` (assets, index.html, wasm with .js and .wasm and .br files) sits a `server` binary. Deploy both, since the server provides the server functions. Running it manually with a default `dioxus::launch` setup reads the `IP` and `PORT` environment variables. In a container (Docker) set `IP=0.0.0.0`, because the default is 127.0.0.1.

## Desktop and mobile bundles
`dx bundle` only builds desktop apps for the native platform and architecture (no macOS app from Windows, etc.); use a CI matrix such as GitHub Actions for cross-builds. Select formats with repeated `--package-types`:
```sh
dx bundle --desktop \
    --package-types "macos" \
    --package-types "dmg"
```
Types: macOS `.app`, `.dmg`; Linux `.appimage`, `.rpm`, `.deb`; Windows `.msi`, `.exe`; iOS `.app`; Android `.apk`. Not every type fits every platform (for example only `.exe` can be built when specifying `--desktop`). Output reports lines like `app - [./target/dx/hot_dog/bundle/macos/bundle/macos/HotDog.app]`.

macOS may require signing and notarizing; mobile apps must be signed. Dioxus has no built-in signing, so use third-party docs (the page links Tauri's signing guides).

## Customize in Dioxus.toml
```toml
[application]
name = "docsite"

[bundle]
identifier = "com.dioxuslabs"
publisher = "DioxusLabs"
icon = ["assets/icon.png"]
```

## JSON mode for automation
Works with all dx commands; most useful with build and bundle. The last emitted line is always the command result.
```sh
dx bundle --desktop \
    --json-output \
    --verbose \
    | tail -1 \
    | jq -r '.json | fromjson | .BundleOutput.bundles []'
```
This prints the bundle paths.

## Checked
Checked 2026-11-07 against the 0.7 Bundling tutorial page (read in full). Confirmed: iOS and Android setup lists, dx bundle --web layout and IP/PORT variables, --package-types list, signing notes, Dioxus.toml bundle section, JSON mode with jq. Corrected: the Windows-only claim for .exe with --desktop (the page does not name Windows) and the wording on the Apple Developer account.
Method: documentation only; no commands were run.
