---
id: computing-software.web-development.vite.troubleshoot-config-cli
name: troubleshoot-config-cli
category: computing-software
field: web-development
product: vite
tags: [esm-only-package, config-esm, ampersand-path-windows, err-require-esm]
level: practitioner
status: docs-checked
description: "Fix 'This package is ESM only' / ERR_REQUIRE_ESM in vite.config by converting the config to ESM, and the Windows '&' in path cannot-find-module error."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ESM-only package errors ("Failed to resolve foo. This package is ESM only but it was tried to load by require", or `ERR_REQUIRE_ESM` from `vite.config.js`): in Node.js 22 and below, ESM files cannot be loaded by `require` by default. It may work with `--experimental-require-module`, with Node.js above 22, or in other runtimes, but the recommendation is to convert the config to ESM by either:
- adding `"type": "module"` to the nearest `package.json`, or
- renaming `vite.config.js` / `.ts` to `vite.config.mjs` / `.mts`.

Windows `Cannot find module '...\foo\bar&baz\vite\bin\vite.js'`: the project path contains `&`, which does not work with `npm` on Windows (npm/cmd-shim#45). Either use another package manager such as `pnpm` or `yarn`, or remove `&` from the path.

The docs also point to Rollup's troubleshooting guide, and to GitHub Discussions or the Vite Land Discord `#help` channel.

## Checked

2026-11-04. Confirmed against the Vite troubleshooting guide (docs/guide/troubleshooting.md, CLI and Config): ESM-only package errors and the two fixes, the Windows ampersand-in-path error and its workarounds, Rollup guide and support channels. Nothing removed.

Method: documentation only; no commands were run.
