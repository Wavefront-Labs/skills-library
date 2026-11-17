---
id: computing-software.web-development.vite.cli-build-options
name: cli-build-options
category: computing-software
field: web-development
product: vite
tags: [vite-build-command, build-flags, ssr-flag, app-flag]
level: practitioner
status: docs-checked
description: "Use vite build CLI flags: target, outDir, assetsDir, assetsInlineLimit, ssr, sourcemap, minify, manifest, ssrManifest, emptyOutDir, watch and app."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vite build [root]` builds for production. Build-specific flags:

- `--target <target>`: default `baseline-widely-available`
- `--outDir <dir>`: default `dist`
- `--assetsDir <dir>`: default `assets`, under outDir
- `--assetsInlineLimit <number>`: base64 inline threshold in bytes, default `4096`
- `--ssr [entry]`: build the entry for server-side rendering
- `--sourcemap [output]`: `true`, `"inline"` or `"hidden"`; default `false`
- `--minify [minifier]`: boolean, `oxc` (default), `terser` or `esbuild`
- `--manifest [name]` and `--ssrManifest [name]`: emit manifest JSON
- `--emptyOutDir`: force-empty an outDir outside root
- `-w, --watch`: rebuild when modules change on disk
- `--app`: build all environments, same as `builder: {}` (experimental)

Shared flags also apply: `-c`, `--base`, `-l`, `--clearScreen`, `--configLoader`, `--profile`, `-d`, `-f`, `-m`.

```bash
vite build --mode staging --sourcemap --manifest
vite build --ssr src/entry-server.js
```

## Checked

2026-11-04. Confirmed against the Vite CLI guide (docs/guide/cli.md, vite build section): every flag, default (baseline-widely-available, dist, assets, 4096, false, oxc) and the minifier values. Nothing removed.

Method: documentation only; no commands were run.
