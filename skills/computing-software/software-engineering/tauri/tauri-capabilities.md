---
id: computing-software.software-engineering.tauri.tauri-capabilities
name: tauri-capabilities
category: computing-software
field: software-engineering
product: tauri
tags: [capabilities, tauri, permissions, acl]
level: practitioner
status: docs-checked
description: "Define Tauri capability files that grant permissions to windows and webviews, target platforms, allow remote URLs, and know what they do not protect."
sources:
  - "https://v2.tauri.app/security/capabilities/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri capabilities

Goal: control which permissions are granted or denied to which windows or webviews. A window or webview in more than one capability merges the permissions and boundaries of all of them.

## Files and enabling

- JSON or TOML files in `src-tauri/capabilities`; one file per capability is good practice.
- All capabilities in that directory are enabled by default. Once any are listed in `tauri.conf.json` under `app > security > capabilities`, only those are used. That array may mix identifier strings with inline capability objects.

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default",
    "core:window:allow-set-title"
  ]
}
```

Inline example: `{ "identifier": "my-capability", "windows": ["*"], "permissions": ["fs:default", "allow-home-read-extended"] }`.

## Commands

By default every command registered with `tauri::Builder::invoke_handler` is allowed for all windows and webviews. To change that, use `AppManifest::commands` in `build.rs`: `tauri_build::Attributes::new().app_manifest(tauri_build::AppManifest::new().commands(&["your_command"]))`.

## Target platform

Add `"platforms"` with any of `linux`, `macOS`, `windows`, `iOS`, `android` (default: all). Use `desktop-schema.json` for desktop capabilities and `mobile-schema.json` for mobile.

## Remote API access

By default the API is reachable only from bundled code. Add `"remote": { "urls": ["https://*.tauri.app"] }` (with `$schema` `remote-schema.json`) to allow remote sources. On Linux and Android, Tauri cannot distinguish requests from an embedded `<iframe>` from those of the window itself.

## What it protects

Protects against: frontend compromise impact, accidental exposure of local interfaces and data, privilege escalation from frontend to backend/system.

Does not protect against: malicious or insecure Rust code, too lax scopes, incorrect scope checks in commands, intentional bypasses from Rust, WebView 0-days or unpatched 1-days, supply chain attacks.

Boundaries depend on window labels, not titles; expose window creation only to higher-privileged windows.

## Schemas

`tauri-build` generates JSON schemas of all available permissions in `gen/schemas`; set `$schema` for IDE autocompletion.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/security/capabilities/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
