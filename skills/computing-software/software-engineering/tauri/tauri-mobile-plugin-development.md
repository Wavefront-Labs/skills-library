---
id: computing-software.software-engineering.tauri.tauri-mobile-plugin-development
name: tauri-mobile-plugin-development
category: computing-software
field: software-engineering
product: tauri
tags: [mobile-plugin-development, tauri, android, ios]
level: advanced
status: docs-checked
description: "Write Kotlin and Swift code for a Tauri plugin: mobile commands, arguments, lifecycle, permissions, events, and calling Rust via JNI or FFI."
sources:
  - "https://v2.tauri.app/develop/plugins/develop-mobile/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile plugin development

Desktop logic lives in `desktop.rs`; `mobile.rs` sends a message to native code. Shared logic goes in `lib.rs`. Add mobile support to an existing plugin with `plugin android init` and `plugin ios init`.

## Plugin classes

- Android: a Kotlin class extending `app.tauri.plugin.Plugin`, annotated `@TauriPlugin`; methods annotated `@Command` take `invoke: Invoke` and finish with `invoke.resolve(JSObject)`.
- iOS: a Swift class extending `Plugin`; commands are `@objc func name(_ invoke: Invoke)` ending in `invoke.resolve([...])`. The plugin is a Swift package.
- Lifecycle: `load` (Android `load(webView: WebView)`, iOS `load(webview: WKWebView)`); Android-only `onNewIntent(intent: Intent)`.

## Threading (Android)

Native commands run on the main thread, so long work can freeze the UI and trigger an ANR. For blocking IO use `CoroutineScope(Dispatchers.IO).launch { ... invoke.resolve(result) }`. For `suspend` functions use a custom `CoroutineScope(Dispatchers.Default + SupervisorJob())`.

## Calling a mobile command from Rust

`self.0.run_mobile_plugin("openCamera", payload)` on `tauri::plugin::PluginHandle`; payload structs use `#[serde(rename_all = "camelCase")]`.

## Arguments

Parse with `invoke.parseArgs(Class)`.

- Android: `@InvokeArg` class (inner objects too). Required `lateinit var x: T`; optional `var x: T? = null`; default `var x: T = value`.
- iOS: `Decodable` class (inner objects too). Required `let x: T`; optional `var x: T?`. Default values are NOT supported; set them in the command function.

## Permissions

- Android: declare in `@TauriPlugin(permissions = [Permission(strings = [Manifest.permission.POST_NOTIFICATIONS], alias = "postNotification")])`.
- iOS: override `checkPermissions` and `requestPermissions`, resolving like `["postNotification": "prompt"]`.
- Tauri auto-adds `checkPermissions` and `requestPermissions` commands, callable from JS (`invoke('plugin:<plugin-name>|checkPermissions')`) or Rust (`run_mobile_plugin`). States starting with `prompt` can be requested; `prompt-with-rationale` means explain first.

## Events

Native code calls `trigger("event", data)` (Android `JSObject`, iOS `data:`). JS listens with `addPluginListener('<plugin-name>', 'event-name', handler)`, which needs the plugin permission (commonly `<plugin-name>:default`) in a capability under `src-tauri/capabilities/`.

## Rust from native code

- Android: add `jni = "0.21"` under `[target.'cfg(target_os = "android")'.dependencies]`; load with `System.loadLibrary("app_lib")`, declare `external fun`, and export `Java_package_class_method` as `#[no_mangle] pub extern "system"`.
- iOS: plain C FFI. Swift declares `@_silgen_name("hello_world_ffi")`; Rust exports a matching `#[no_mangle] pub unsafe extern "C"` function, plus a free function for returned strings.

## 16KB pages

NDK 28+ should align automatically; otherwise set `rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]` under `[target.aarch64-linux-android]` in `.cargo/config.toml`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/plugins/develop-mobile/ (page text including code blocks and tabs read in full).
Fixed a formatting join between the Android and iOS bullets.
Method: documentation only; no commands were run.
