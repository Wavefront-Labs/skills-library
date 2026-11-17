---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-write-custom-plugin
name: tauri-write-custom-plugin
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-write-custom-plugin, tauri-plugins, tauri, tauri2, plugins, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Scaffold a Tauri plugin with plugin new, add commands and autogenerate their permissions in build.rs."
sources:
  - https://v2.tauri.app/develop/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write a custom Tauri plugin

**Goal:** reusable native functionality.

```bash
npx @tauri-apps/cli plugin new my-plugin     # creates tauri-plugin-my-plugin/
```

```rust
// src/lib.rs
use tauri::{plugin::{Builder, TauriPlugin}, Runtime};
pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![commands::upload])
        .build()
}
// build.rs
const COMMANDS: &[&str] = &["upload"];
fn main() { tauri_plugin::Builder::new(COMMANDS).build(); }
// JS binding: invoke('plugin:my-plugin|upload', { ... })
```

**Gotcha:** commands are not reachable from the frontend until permissions allow them. Listing the snake_case command names in `COMMANDS` in `build.rs` generates `allow-<command>` and `deny-<command>` permissions; add the allow permission (or a `default` permission set in `permissions/`) so apps can grant it. Plugin names must be lowercase ASCII letters, digits and hyphens, with no leading or trailing hyphen.

## Verify
- The plugin loads and the command succeeds once a capability grants its permission.

## Checked
2026-11-03. Confirmed in the Tauri plugin development page: `plugin new`, the `tauri-plugin-<name>` crate naming and identifier rules, `Builder::new(...).invoke_handler(generate_handler![...])`, `TauriPlugin<R>` returned from an `init` function, the `plugin:<name>|<command>` invoke form, denied-by-default commands, and `COMMANDS` in `build.rs` generating allow and deny permissions. Removed: the `ping` command and the app-side `.plugin(tauri_plugin_my_plugin::init())` line (not shown for custom plugins on the page).
Method: documentation only; no commands were run.
