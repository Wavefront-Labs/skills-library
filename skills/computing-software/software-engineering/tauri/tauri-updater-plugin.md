---
id: computing-software.software-engineering.tauri.tauri-updater-plugin
name: tauri-updater-plugin
category: computing-software
field: software-engineering
product: tauri
tags: [updater-plugin, tauri, updates, signing]
level: advanced
status: docs-checked
description: "Set up the Tauri updater plugin: signing keys, tauri.conf.json, static JSON or dynamic server responses, and checking and installing updates."
sources:
  - "https://v2.tauri.app/plugin/updater/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri updater plugin

Goal: update an installed app from an update server or a static JSON file.

## Setup and signing

Install with `pnpm tauri add updater` (or the npm/yarn/cargo equivalent). Manually: `cargo add tauri-plugin-updater --target 'cfg(any(target_os = "macos", windows, target_os = "linux"))'`, then in `setup` call `app.handle().plugin(tauri_plugin_updater::Builder::new().build())` under `#[cfg(desktop)]`.

Signing cannot be disabled. Generate keys with `tauri signer generate -w ~/.tauri/myapp.key`. The public key goes in `tauri.conf.json`; never share the private key, and losing it means you cannot publish updates to installed apps. When building, set `TAURI_SIGNING_PRIVATE_KEY` (path or content) and optionally `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` in the environment; `.env` files do not work.

## Configuration

```json
{
  "bundle": { "createUpdaterArtifacts": true },
  "plugins": {
    "updater": {
      "pubkey": "CONTENT FROM PUBLICKEY.PEM",
      "endpoints": ["https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}"]
    }
  }
}
```

- Use `"v1Compatible"` for `createUpdaterArtifacts` when migrating from v1; it will be removed in v3.
- `pubkey` cannot be a file path. Endpoints need TLS in production (`dangerousInsecureTransportProtocol` overrides); the next URL is tried only on a non-2XX status.
- URL variables: `{{current_version}}`, `{{target}}` (`linux`, `windows`, `darwin`), `{{arch}}` (`x86_64`, `i686`, `aarch64`, `armv7`). Custom variables are not supported.
- Windows `plugins.updater.windows.installMode`: `"passive"` (default), `"basicUi"`, `"quiet"`.

## Server responses

Static JSON requires `version` (SemVer), and `platforms.<OS-ARCH>.url` and `.signature` (the content of the `.sig` file, not a path or URL); `notes` and `pub_date` (RFC 3339) are optional. The whole file is validated before the version is checked.

Dynamic server: reply `204 No Content` when there is no update, else `200 OK` with JSON containing `version`, `url`, `signature` (optional `notes`, `pub_date`).

## Checking and installing

```js
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update) {
  await update.downloadAndInstall();
  await relaunch();
}
```

Rust: `app.updater()?.check().await?` then `update.download_and_install(on_chunk, on_finish).await?` and `app.restart()`. On Windows the app exits automatically at install. `check` accepts `proxy`, `timeout` and `headers`.

Rust-only runtime options on `updater_builder()`: `endpoints`, `pubkey`, `target` (custom, matched against the static JSON platform key), `version_comparator` (default `update.version > current`; use `update.version != current` to allow downgrades) and `on_before_exit`. Config values are the fallback. Grant `updater:default` in your capability.

## Checked

Checked 2026-11-08 against the Tauri v2 updater plugin page: install commands, signing and environment variables, createUpdaterArtifacts, pubkey and endpoints rules, URL variables and values, Windows installMode, static JSON and dynamic server response rules, JavaScript and Rust check and install calls, runtime builder options, and the updater:default permission. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
