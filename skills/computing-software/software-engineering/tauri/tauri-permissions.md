---
id: computing-software.software-engineering.tauri.tauri-permissions
name: tauri-permissions
category: computing-software
field: software-engineering
product: tauri
tags: [permissions, tauri, security, capabilities]
level: practitioner
status: docs-checked
description: "Define Tauri permissions and permission sets in TOML, name them with valid identifiers, and lay out the files for a plugin or an app."
sources:
  - "https://v2.tauri.app/security/permissions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri permissions

Goal: describe the privileges of commands so the frontend can use them, then reference them from a capability.

## What a permission is

A permission can enable or deny commands, define scopes, or both. To grant or deny one to a window or webview, reference it in a capability.

```toml
[[permission]]
identifier = "my-identifier"
description = "This describes the impact and more."
commands.allow = [
    "read_file"
]

[[permission.scope.allow]]
my-scope = "$HOME/*"

[[permission.scope.deny]]
my-scope = "$HOME/secret"
```

## Identifiers

- `<name>:default` is the default permission of a plugin or app.
- `<name>:<command-name>` is the permission for one command.

`<name>` is the plugin crate name without the `tauri-plugin-` prefix, which is prepended automatically at compile time. It is not needed for the app's own permissions. Identifiers use ASCII lowercase `[a-z]` only, with a maximum length of 116.

## Permission sets

Group permissions under a new identifier to combine scope permissions with command permissions or bundle OS-specific ones.

```toml
[[set]]
identifier = "allow-home-read-extended"
description = "Non-recursive read access to files and mkdir in $HOME."
permissions = [
    "fs:read-files",
    "fs:scope-home",
    "fs:allow-mkdir"
]
```

## File layout

- Plugin: `permissions/<identifier>.json/toml` and `permissions/default.json/toml`. The default permission is added to the app configuration automatically when plugins are added with the Tauri CLI.
- App: `src-tauri/permissions/<identifier>.toml` plus `src-tauri/capabilities/<identifier>.json/.toml`.

Capability files may be json, json5 or toml. Permissions can only be defined in toml.

## Checked
2026-11-08. Read the Tauri v2 security permissions page (tauri-docs, v2 branch) in full; claims match.
Method: documentation only; no commands were run.
