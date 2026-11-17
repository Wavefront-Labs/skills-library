---
id: computing-software.software-engineering.tauri.tauri-asset-protocol
name: tauri-asset-protocol
category: computing-software
field: software-engineering
product: tauri
tags: [asset-protocol, tauri, security, fsscope]
level: practitioner
status: docs-checked
description: "Configure app.security.assetProtocol with an FsScope so the Tauri webview can load local files, including deny rules and leading-dot handling on Unix."
sources:
  - "https://v2.tauri.app/security/asset-protocol/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri asset protocol scope

Goal: let the webview load local files (for example via `convertFileSrc`) through the asset protocol, within a narrow scope.

## Method

In `tauri.conf.json` set `app.security.assetProtocol.enable` to `true` and define a `scope`. Paths resolved at runtime must match it or the load is refused ("asset protocol not configured to allow the path"). CSP for `asset:` sources is on the CSP page.

`scope` is an `FsScope`: an array of glob patterns, or an object with `allow`, optional `deny`, and optional `requireLiteralLeadingDot`. `deny` wins over `allow`. Patterns may start with a base directory variable such as `$HOME`, `$CACHE`, `$APPCACHE`, `$APPDATA`, `$RESOURCE`.

Resolved paths are usually absolute, so `["*/**"]` typically does not match. Use `$HOME/**/*` or a pattern mirroring the resolved path.

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": {
          "allow": ["$APPCACHE/**/*"],
          "deny": ["$APPCACHE/**/secrets/**"]
        }
      }
    }
  }
}
```

The array form (`["$APPCACHE/**/*", "$RESOURCE/**/*"]`) cannot set `requireLiteralLeadingDot`.

## Dot-prefixed segments on Unix

`requireLiteralLeadingDot` defaults to `true` on Unix, so `*`, `?`, `**` and `[...]` do not match a component starting with `.`. `$HOME/**` will not match a file under `.cache`, but `$HOME/.cache/myapp/**` will. Setting it to `false` (object form only) widens access; review carefully.

## Other points

- Prefer `**/*` over bare `**` for "all files under here".
- Prefer narrow directories (`$APPCACHE`, `$RESOURCE`) over `$HOME/**/*` or `**/*`.
- Runtime-chosen paths (for example from the dialog plugin) need the persisted-scope plugin; enable its `protocol-asset` feature and register `tauri_plugin_fs` before `tauri_plugin_persisted_scope`:

```toml
tauri-plugin-persisted-scope = { version = "2", features = ["protocol-asset"] }
```

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/security/asset-protocol/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
