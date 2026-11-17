---
id: computing-software.software-engineering.wails.mobile-support
name: mobile-support
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, v3, mobile, ios, android, experimental]
level: practitioner
status: docs-checked
description: "Build and run an experimental Wails v3 app on iOS and Android: prerequisites, task commands, per-platform options, platform detection, limits and common build errors."
sources: [https://wails.io/docs/guides/mobile]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails v3 mobile builds (experimental)

Goal: ship the same Go + web frontend app to iOS and Android. The page marks this EXPERIMENTAL: the API and build process may change before the final release.

## Architecture

iOS uses WKWebView with a CGO bridge (output .app / .ipa). Android uses Android WebView with JNI (output .apk).

## Prerequisites

- iOS: macOS 12+, Xcode 14+, Go 1.21+ with CGO. macOS is required.
- Android (macOS, Linux or Windows): Go 1.21+ with CGO, Android SDK (platform tools/adb, build tools, optional emulator; API 34 or later platform), Android NDK r26d or later, JDK 11+.
- Environment (shell profile):
  ```bash
  export ANDROID_HOME="$HOME/Library/Android/sdk"   # macOS; Linux: $HOME/Android/Sdk
  export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/29.0.14206865"   # adjust version
  export PATH=$PATH:$ANDROID_HOME/platform-tools
  export PATH=$PATH:$ANDROID_HOME/emulator
  ```

## Build and run

```bash
task ios:build            # task ios:run for simulator, task ios:build:device needs code signing
task android:build        # default arm64 device
task android:build ARCH=x86_64      # emulator
task android:compile:go:all-archs
task android:package      # APK
task android:run
task android:logs
```
iOS builds compile Go to a static library, generate an Xcode project, and use `xcodebuild`. Android compiles Go to a `.so`, builds the Java/Kotlin part with Gradle, and packages an APK. Android ABIs: arm64-v8a (GOARCH arm64, modern devices), x86_64 (amd64, emulator), armeabi-v7a (arm) and x86 (386) optional. Simulator/emulator helpers: `xcrun simctl list devices`, `task ios:run SIMULATOR="iPhone 15 Pro"`, `emulator -list-avds`, `emulator -avd Pixel_7_API_34`.

## Options

Set under `application.Options`: `iOS: application.IOSOptions{DisableBounce, EnableZoom, UserAgent, BackgroundColour}` and `Android: application.AndroidOptions{DisableScroll, DisableOverscroll, EnableZoom, UserAgent, BackgroundColour, DisableHardwareAcceleration}` (the last is not recommended).

Detect the platform in the frontend:
```javascript
const platform = window.wails.System.Platform(); // 'ios', 'android', else desktop
```

## Limitations

The page lists these as not yet fully implemented. Both: system tray (not applicable), multiple windows (single full-screen window only). iOS: file dialogs (limited by sandboxing), window manipulation (position, size). Android: file dialogs (use Storage Access Framework), window manipulation (fullscreen only), clipboard (partial support).

## Troubleshooting stated by the page

- Code signing required: needs an Apple Developer account for physical devices; simulators do not.
- Command Line Tools not found: `xcode-select --install`.
- NDK not found: check `ls $ANDROID_HOME/ndk`, set `ANDROID_NDK_HOME` explicitly.
- UnsatisfiedLinkError dlopen failed: architecture mismatch; rebuild for arm64 (device) or x86_64 (emulator).
- Blank WebView: enable WebView debugging in dev builds, use `chrome://inspect/#devices`, read `task android:logs`.
- cannot find package: `go clean -modcache`, `go mod tidy`, `go mod download`. CGO_ENABLED required: `export CGO_ENABLED=1`.

Examples live at `v3/examples/ios/` and `v3/examples/android/` in the repository.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Mobile Support" guide.

Corrected or removed: Re-stated the limitations the way the page lists them (not yet fully implemented, system tray not applicable) instead of the blanket "no" wording, and added the Android window and clipboard limits.

Method: documentation only; no commands were run.
