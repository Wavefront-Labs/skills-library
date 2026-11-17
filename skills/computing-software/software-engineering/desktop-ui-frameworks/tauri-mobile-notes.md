---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-mobile-notes
name: tauri-mobile-notes
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-mobile-notes, tauri-bundling, tauri, tauri2, bundling, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Write Tauri 2 Rust that builds for desktop and mobile: mobile entry point, cfg(desktop) gating and plugin platform support."
sources:
  - https://v2.tauri.app/plugin/updater/
  - https://v2.tauri.app/develop/plugins/
  - https://v2.tauri.app/plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri 2 mobile notes

**Goal:** keep one codebase building for desktop and mobile.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            #[cfg(desktop)]
            app.handle().plugin(tauri_plugin_updater::Builder::new().build());
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Gotcha:** some plugins support only desktop (the updater is added with `#[cfg(desktop)]` and a `cfg(any(target_os = "macos", windows, target_os = "linux"))` dependency target), so gate them. Each plugin's page has a platform support table, and a plugin declares its own levels (full, partial, none) per platform. A plugin can ship Kotlin (Android) and Swift (iOS) code; add them to an existing plugin with `plugin android add` and `plugin ios add`.

## Verify
- The project compiles for the target with desktop-only code excluded.

## Checked
2026-11-03. Confirmed in the Tauri updater and plugin development pages: `#[cfg_attr(mobile, tauri::mobile_entry_point)]`, `#[cfg(desktop)]` gating, the desktop-only dependency target, `[package.metadata.platforms.support]` levels, plugin Kotlin and Swift libraries, and `plugin android add` / `plugin ios add`. Removed: the `android init`/`android dev`/`ios init`/`ios dev` commands, "needs macOS + Xcode" for iOS, and "windows, tray, sidecars do not exist on mobile" (the mobile guide page returned 404 and the other pages do not state these), plus the `cfg(mobile)` advice. The description no longer promises a mobile build walkthrough.
Method: documentation only; no commands were run.
