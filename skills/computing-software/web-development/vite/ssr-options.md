---
id: computing-software.web-development.vite.ssr-options
name: ssr-options
category: computing-software
field: web-development
product: vite
tags: [ssr-external-option, ssr-no-external-option, ssr-target-option, ssr-resolve-external-conditions, ssr-main-fields]
level: advanced
status: docs-checked
description: "Config ssr.external, noExternal precedence rules, ssr.target, ssr.resolve conditions and externalConditions (matching node --conditions), and SSR mainFields."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/ssr-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applied to dev and build.

- `ssr.external` (`string[] | true`): externalize deps and their transitive deps. By default all are, except linked deps (for HMR). `true` externalizes linked ones too. An explicit `string[]` entry beats `ssr.noExternal`.
- `ssr.noExternal` (`string | RegExp | (string | RegExp)[] | true`): bundle these in build. `true` externalizes nothing, though explicit `ssr.external` string lists can still win; with both `true`, `noExternal` wins. With `ssr.target: 'node'`, Node built-ins stay external.
- `ssr.target` (`'node' | 'webworker'`, default `node`).
- `ssr.resolve.conditions`: default `['module', 'node', 'development|production']` (`['module', 'browser', 'development|production']` for `webworker`); only non-externalized deps.
- `ssr.resolve.externalConditions`: default `['node', 'module-sync']`, for imports of externalized direct deps including `ssrLoadModule`. Run Node with the same `--conditions` in dev and after build:

```sh
NODE_OPTIONS='--conditions custom' vite
```

- `ssr.resolve.mainFields`: default `['module', 'jsnext:main', 'jsnext']`; lower precedence than `exports`; non-externalized deps only.

## Checked

2026-11-04. Confirmed against the Vite SSR options page (docs/config/ssr-options.md): external, noExternal precedence rules, target, resolve.conditions and externalConditions defaults, the NODE_OPTIONS conditions tip, mainFields. Nothing removed.

Method: documentation only; no commands were run.
