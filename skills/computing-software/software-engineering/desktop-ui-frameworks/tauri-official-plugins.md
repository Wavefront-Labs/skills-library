---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-official-plugins
name: tauri-official-plugins
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-official-plugins, tauri-plugins, tauri, tauri2, plugins, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Add an official Tauri 2 plugin (shell as the example) with tauri add, register it and grant its permission."
sources:
  - https://v2.tauri.app/plugin/
  - https://v2.tauri.app/plugin/shell/
  - https://v2.tauri.app/develop/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri official plugins

**Goal:** use maintained building blocks.

```bash
npm run tauri add shell          # automatic setup (yarn, pnpm, deno, bun and cargo equivalents exist)
# manual, from src-tauri:
cargo add tauri-plugin-shell
npm install @tauri-apps/plugin-shell
```

```rust
// lib.rs
tauri::Builder::default().plugin(tauri_plugin_shell::init())
```

```json
// src-tauri/capabilities/default.json
{ "permissions": ["shell:default"] }
```

**Gotcha:** plugin commands and scopes that are potentially dangerous are blocked by default, so a freshly added plugin needs its permissions listed in a capability. Check the plugin's page for its identifiers and its supported platforms: the plugins index lists many official plugins (for example dialog, fs, shell and store) with per-platform support.

## Verify
- The plugin command works after granting its permission.

## Checked
2026-11-03. Confirmed in the Tauri plugins index, the shell plugin page and the plugin development page: `tauri add <plugin>`, the manual `cargo add tauri-plugin-shell` and `@tauri-apps/plugin-shell` install, `.plugin(tauri_plugin_shell::init())`, blocked-by-default permissions and the capabilities file, the existence of dialog, fs, shell and store plugins, and per-platform support. Removed: the `store:default` identifier, the `tauri_plugin_store::Builder` registration, the `Store` import and the claim that `tauri add` adds a capability stub (none of these are shown on the pages read), and the "not allowed" error wording. The shell example replaces the original store example.
Method: documentation only; no commands were run.
