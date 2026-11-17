---
id: computing-software.web-development.vite.config-file-basics
name: config-file-basics
category: computing-software
field: web-development
product: vite
tags: [vite-config-file, define-config, satisfies-user-config, config-loader-native]
level: intro
status: docs-checked
description: "Write vite.config: file resolution and ESM rules, --config, defineConfig or JSDoc typing, TypeScript configs with satisfies, and bundle versus native config loader."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite looks for `vite.config.js` (other JS and TS extensions work) in the project root. To use ES module syntax the file must be detected as ESM by Node.js: `.mjs`, or `.js` with `"type": "module"` in the closest `package.json`. Choose another file with `vite --config my-config.js` (relative to `cwd`).

Typing:

```js
import { defineConfig } from 'vite'
export default defineConfig({ /* ... */ })
```

or `/** @type {import('vite').UserConfig} */`, or in TypeScript `export default { } satisfies UserConfig` with `import type { UserConfig } from 'vite'`.

Loading: by default Vite bundles the config with Rolldown into a temporary file and loads it. In an environment that supports TypeScript (Node 22.18+) or with plain JS, `--configLoader native` uses the native runtime; the docs say it is planned to become the default in a future major.

## Checked

Date: 2026-11-07. Read config/index.md in full (opening, CONFIG LOADING tip, Config Intellisense). File resolution, ESM detection, `--config`, `defineConfig`, JSDoc and `satisfies UserConfig` typing, Rolldown-bundled loading and `--configLoader native` with Node 22.18+ all matched; nothing trimmed.

Method: documentation only; no commands were run.
