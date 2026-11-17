---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-capabilities-config
name: tauri-capabilities-config
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-capabilities-config, tauri-security, tauri, security, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Grant windows specific permissions through capability files in src-tauri/capabilities."
sources:
  - https://v2.tauri.app/security/capabilities/
  - https://v2.tauri.app/security/permissions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri capability files

**Goal:** least-privilege frontend.

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:window:allow-set-title"
  ]
}
```

**Gotcha:** a permission only applies to a window or webview once a capability references it. Files in `src-tauri/capabilities` are all enabled by default, but once `app.security.capabilities` in `tauri.conf.json` lists any, only those are used. A window in more than one capability gets the merged permissions of all of them, and boundaries follow window labels, not titles. Capabilities do not protect against insecure Rust code or scopes that are too lax.

## Verify
- A window whose label is not in a capability's `windows` list cannot use that capability's permissions.

## Checked
2026-11-03. Confirmed in the Tauri capabilities and permissions pages: capability files as JSON or TOML in `src-tauri/capabilities`, the `identifier`, `windows`, `permissions` and `platforms` fields, the `$schema` files generated under `gen/schemas`, the `core:` permission identifiers shown, the enabled-by-default and `app.security.capabilities` behaviour, merging across capabilities, window labels, and the listed non-protections. Removed: the `fs:allow-read-text-file` and `fs:scope` entries with a `$APPDATA` path (not on the pages read) and the claim that a permission error from `invoke` usually means a missing identifier.
Method: documentation only; no commands were run.
