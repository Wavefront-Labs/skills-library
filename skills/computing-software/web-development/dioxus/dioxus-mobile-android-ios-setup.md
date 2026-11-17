---
id: computing-software.web-development.dioxus.dioxus-mobile-android-ios-setup
name: dioxus-mobile-android-ios-setup
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, mobile, android, ios, dx-serve, ndk-home, rustup-target, xcode]
level: practitioner
status: docs-checked
description: "Set up Android (SDK, NDK, rustup targets, env vars) and iOS (Xcode, targets) and run a Dioxus app on an emulator or simulator with dx serve."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/platforms/mobile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus mobile setup (Android and iOS)

Goal: build and run a Dioxus app on an Android emulator or iOS simulator. Since Dioxus 0.6, `dx` has built-in mobile support.

## Android

```sh
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android
```

1. Install Android Studio.
2. Create a blank Android project, open `Tools > SDK manager`, go to `SDK tools`.
3. Select the SDK, the SDK command line tools, the NDK (side by side) and CMAKE, then apply.
4. Set `JAVA_HOME`, `ANDROID_HOME` and `NDK_HOME`, and add the emulator and platform-tools directories to `PATH`. Example (Mac):

```sh
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
export ANDROID_HOME="$HOME/Library/Android/sdk"
export NDK_HOME="$ANDROID_HOME/ndk/25.2.9519653"
export PATH="$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools"
```

The NDK version in the path must match the version you installed. PATH is set manually because some Android Studio distributions put the emulator in the wrong location.

## iOS

Install Xcode, the iOS SDK and the Xcode command line tools, then:

```sh
rustup target add aarch64-apple-ios aarch64-apple-ios-sim
```

On an M1 Mac, to run in the simulator use `cargo build --target x86_64-apple-ios` instead of `cargo apple build`.

## Run

```sh
dx new my-app
```

Start a simulator first. Android: `emulator -avd Pixel_6_API_34  -netdelay none -netspeed full` (adjust the device name). iOS:

```sh
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
xcrun simctl boot "iPhone 15 Pro Max"
```

Then `cd my-app` and `dx serve` to start the app in development mode.

## Gotcha

Mobile renders through the platform WebView (or experimentally WGPU). Native Android animations and widgets are not supported; use CSS animations and styling instead.

## Checked
Checked 2026-11-07 against the 0.7 Mobile guide (read in full). Confirmed: Android and iOS rustup targets, SDK manager steps, Mac environment variables and NDK version match, PATH note, M1 simulator note, emulator and simctl commands, dx new and dx serve, WebView or WGPU and the CSS animation note. The page also has Windows variable commands, which the skill does not cover. Nothing removed.
Method: documentation only; no commands were run.
