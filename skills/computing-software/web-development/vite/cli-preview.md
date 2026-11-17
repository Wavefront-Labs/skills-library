---
id: computing-software.web-development.vite.cli-preview
name: cli-preview
category: computing-software
field: web-development
product: vite
tags: [vite-preview-command, preview-build, optimize-deprecated]
level: intro
status: docs-checked
description: "Preview a production build locally with vite preview, know its flags, and know vite optimize is deprecated."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vite preview [root]` serves the build directory (default `dist`) locally. Run `vite build` first so the directory is current. It is not designed as a production server. It applies certain middleware depending on the configured `appType`.

Options: `--host [host]`, `--port <port>`, `--strictPort`, `--open [path]`, `--outDir <dir>` (default `dist`), plus the shared `-c`, `--base`, `-l`, `--clearScreen`, `--configLoader`, `-d`, `-f`, `-m`.

```bash
vite build && vite preview --port 4173 --open
```

`vite optimize [root]` pre-bundles dependencies (flags: `--force` and the shared ones). It is deprecated: the pre-bundle process runs automatically and does not need to be called.

## Checked

2026-11-04. Confirmed against the Vite CLI guide (docs/guide/cli.md, vite preview and vite optimize sections): flags, default dist, not-a-production-server note, appType middleware, optimize deprecation. Nothing removed.

Method: documentation only; no commands were run.
