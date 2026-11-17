---
id: computing-software.web-development.vite.troubleshoot-hmr
name: troubleshoot-hmr
category: computing-software
field: web-development
product: vite
tags: [hmr-not-working, full-reload, circular-dependency-hmr, import-case-mismatch]
level: practitioner
status: docs-checked
description: "Diagnose HMR problems: wrong-case imports, unhandled HMR causing full reloads, circular dependencies, and vite --debug hmr to log the cycle."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite detects a change but HMR does not work: you may be importing a file with different case. If `src/foo.js` exists:

```js
import './Foo.js' // should be './foo.js'
```

Vite does not detect changes at all: under WSL2 it cannot watch in some conditions; see `server.watch`.

A full reload happens instead of HMR:
- If neither Vite nor a plugin handles HMR for the module, a full reload is the only way to refresh state.
- If HMR is handled but sits inside a circular dependency, a full reload also happens to recover execution order. Break the loop. `vite --debug hmr` logs the circular dependency path when a file change triggered it.

Related: case mismatches also cause `ENOENT` / `Module not found` when you build on case-sensitive Linux after developing on Windows or macOS.

## Checked

2026-11-07. Re-read the Vite Troubleshooting guide (docs/guide/troubleshooting.md) in full, HMR and Build sections. Confirmed the wrong-case import example, the WSL2 watch pointer, the two causes of a full reload instead of HMR, vite --debug hmr for circular dependency paths, and the related case-sensitivity ENOENT note. Nothing removed.

Method: documentation only; no commands were run.
