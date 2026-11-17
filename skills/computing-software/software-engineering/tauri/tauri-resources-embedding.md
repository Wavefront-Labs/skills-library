---
id: computing-software.software-engineering.tauri.tauri-resources-embedding
name: tauri-resources-embedding
category: computing-software
field: software-engineering
product: tauri
tags: [resources-embedding, tauri]
level: practitioner
status: draft
description: "Bundle extra files into a Tauri app with bundle.resources, resolve their paths in Rust or JavaScript, and allow access through capabilities."
sources:
  - "https://v2.tauri.app/develop/resources/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedding additional files (resources)

Goal: ship files that are not part of `frontendDist` or are too big to inline.

## Configure

List files in `bundle.resources` of `tauri.conf.json`:

```json
{ "bundle": { "resources": ["./path/to/some-file.txt", "some-folder/", "resources/**/*.md"] } }
```

- Relative paths keep their structure under `$RESOURCE`. `..` becomes `_up_`; the root of an absolute path becomes `_root_`.
- `dir/` copies recursively; `dir/*` copies files non-recursively; `dir/**/*` copies all files recursively; `dir/**` alone throws an error.
- To control destinations, use a map: `{ "resources/": "", "docs/**/*md": "website-docs/" }`. Glob matches in a map land flat in the target directory, without their folder structure.

## Resolve paths

- Rust: `app.path().resolve("lang/de.json", BaseDirectory::Resource)?` (from `App` or `AppHandle`). The path follows the same syntax as `bundle > resources`.
- JavaScript: `import { resolveResource } from '@tauri-apps/api/path'; const p = await resolveResource('lang/de.json');`
- Android: resources are stored as APK assets, so results use the `asset://localhost/` prefix; read with the `fs` plugin (`app.fs().read_to_string(&path)`) rather than `std::fs`.

## Read from JavaScript

With the `fs` plugin set up, add permissions to `src-tauri/capabilities/default.json`:

```json
"permissions": ["core:default", "fs:allow-read-text-file", "fs:allow-resource-read-recursive"]
```

Then `JSON.parse(await readTextFile(await resolveResource('lang/de.json')))`. Alternatively, write a command that reads the file in Rust and `invoke` it.

## Permissions for `_up_` and `_root_` files

Use `$RESOURCE/**/*` to allow recursive access, for example an `fs:scope` permission with `"allow": ["$RESOURCE/**/*"]` and `"deny": ["$RESOURCE/secret.txt"]` (add `fs:allow-stat`, `fs:allow-read-text-file`, `fs:allow-resource-read-recursive`), or `opener:allow-open-path` with `"allow": [{ "path": "$RESOURCE/**/*" }]` for the opener plugin.
