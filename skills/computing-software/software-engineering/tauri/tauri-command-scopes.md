---
id: computing-software.software-engineering.tauri.tauri-command-scopes
name: tauri-command-scopes
category: computing-software
field: software-engineering
product: tauri
tags: [command-scopes, tauri, security, permissions]
level: practitioner
status: docs-checked
description: "Define allow and deny scopes for Tauri commands, merge them into permission sets, and scope a plugin's read access to a folder."
sources:
  - "https://v2.tauri.app/security/scope/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri command scopes

Goal: restrict what a Tauri command may do, such as which paths or URLs it may touch.

## Rules

- A scope is either `allow` or `deny`; `deny` always supersedes `allow`.
- The scope type can be any `serde` serializable type, and is plugin-specific in general. For scoped commands in your own app, define the type in the app and enforce it in the command implementation.
- The scope is passed to the command, and the command itself must enforce it. Command developers must ensure no scope bypass is possible and should audit the validation.
- The `fs` plugin scopes directories and files; the `http` plugin scopes reachable URLs.

## Example (fs plugin)

The fs scope type is a string holding a `glob` compatible path.

```toml
[[permission]]
identifier = "scope-applocaldata-recursive"
description = "Recursive access to the complete $APPLOCALDATA folder."

[[permission.scope.allow]]
path = "$APPLOCALDATA/**"
```

A deny scope can be limited per platform:

```toml
[[permission]]
identifier = "deny-webview-data-windows"
description = "Denies read access to the webview data folder on windows."
platforms = ["windows"]

[[permission.scope.deny]]
path = "$APPLOCALDATA/EBWebView/**"
```

## Merging into sets

Merge scopes to cut duplicate configuration:

```toml
[[set]]
identifier = "deny-default"
description = "Denies access to dangerous Tauri relevant files and folders by default."
permissions = ["deny-webview-data-linux", "deny-webview-data-windows"]

[[set]]
identifier = "scope-applocaldata-reasonable"
description = "Allows APPLOCALDATA with the default denies."
permissions = ["scope-applocaldata-recursive", "deny-default"]

[[set]]
identifier = "read-files-applocaldata"
description = "File read access to APPLOCALDATA and subfolders."
permissions = ["scope-applocaldata-reasonable", "allow-read-file"]
```

Scopes apply to all commands by extending the plugin's global scope, or only to selected commands when combined with an enabled command inside a permission.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/security/scope/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
