---
id: computing-software.software-engineering.tauri.tauri-file-system-plugin
name: tauri-file-system-plugin
category: computing-software
field: software-engineering
product: tauri
tags: [fs-plugin, tauri, filesystem, scopes]
level: practitioner
status: docs-checked
description: "Use the Tauri fs plugin from JavaScript: base directories, reading, writing, opening, watching, and the capability permissions plus scopes it needs."
sources:
  - "https://v2.tauri.app/plugin/file-system/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri file system plugin

Goal: read and write files from the frontend within an explicit scope. In Rust use `std::fs` or `tokio::fs`; the plugin's Rust side only changes scope permissions.

## Setup

`pnpm tauri add fs`, or manually `cargo add tauri-plugin-fs`, `.plugin(tauri_plugin_fs::init())` in `lib.rs`, and `pnpm add @tauri-apps/plugin-fs`.

- Android: for audio, cache, documents, downloads, picture, public or video directories add `READ_EXTERNAL_STORAGE` and `WRITE_EXTERNAL_STORAGE` `uses-permission` entries to `gen/android/app/src/main/AndroidManifest.xml`.
- iOS: create `src-tauri/gen/apple/PrivacyInfo.xcprivacy` declaring `NSPrivacyAccessedAPICategoryFileTimestamp` with reason `C617.1`.

## Paths

Parent accessors (`..`) are not allowed. Paths are relative to a base directory or built with the path API.

```js
import { readFile, BaseDirectory } from '@tauri-apps/plugin-fs';
const contents = await readFile('avatars/tauri.png', { baseDir: BaseDirectory.Home });
```

## Common calls

- `create(path, opts)` returns a handle, truncating an existing file. Always `file.close()`.
- `writeTextFile` / `writeFile`, `readTextFile` / `readFile`; `readTextFileLines` streams lines.
- `open(path, opts)`: options `read` (default), `write`, `append`, `truncate` (needs `write`), `create` (needs `write` or `append`), `createNew` (fails if present). Always `file.close()`.
- `copyFile` and `rename` take `fromPathBaseDir` and `toPathBaseDir`.
- `remove` (needs `recursive: true` for non-empty directories), `exists`, `mkdir`, `readDir`, `truncate`, `stat` (follows symlinks) and `lstat` (does not).
- `watch` (debounced, `delayMs`) and `watchImmediate`; non-recursive unless `recursive: true`. Needs `tauri-plugin-fs = { version = "2.0.0", features = ["watch"] }`.

## Permissions need scopes

A permission such as `fs:allow-exists` alone allows no path and fails at runtime with a `forbidden path` error. Add an allow scope:

```json
{
  "permissions": [
    "fs:default",
    {
      "identifier": "fs:allow-exists",
      "allow": [{ "path": "$APPDATA/*" }]
    }
  ]
}
```

Use `fs:scope` to apply a scope to every `fs` command. Scope entries are `{ path: string }`; `deny` beats `allow`. Variables include `$APPCONFIG`, `$APPDATA`, `$APPLOCALDATA`, `$APPCACHE`, `$APPLOG`, `$AUDIO`, `$CACHE`, `$CONFIG`, `$DATA`, `$LOCALDATA`, `$DESKTOP`, `$DOCUMENT`, `$DOWNLOAD`, `$EXE`, `$FONT`, `$HOME`, `$PICTURE`, `$PUBLIC`, `$RUNTIME`, `$TEMPLATE`, `$VIDEO`, `$RESOURCE`, `$TEMP`.

On Unix, dotfiles and dotfolders need the full path or a glob after the dotfolder component; otherwise set `"plugins": { "fs": { "requireLiteralLeadingDot": false } }` in `tauri.conf.json`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/plugin/file-system/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
