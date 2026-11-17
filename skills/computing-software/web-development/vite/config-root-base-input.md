---
id: computing-software.web-development.vite.config-root-base-input
name: config-root-base-input
category: computing-software
field: web-development
product: vite
tags: [root-option, base-values, mode-option, input-option]
level: practitioner
status: docs-checked
description: "Core shared options: root, base values (pathname, full URL, empty or ./), mode override for serve and build, and the input entry default for build, lib, ssr and optimizeDeps."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shared options apply to dev, build and preview unless noted.

- `root`: string, default `process.cwd()`. Project root where `index.html` is; absolute or relative to cwd.
- `base`: string, default `/`. Valid: absolute pathname like `/foo/`; full URL like `https://bar.com/foo/` (origin is unused in dev); empty string or `./` for embedded deployment. Related to `server.origin`.
- `mode`: default `'development'` for serve, `'production'` for build. Setting it in config overrides both; the `--mode` CLI flag overrides this.
- `input`: `string | string[] | { [entryAlias]: string }`, resolved from the root. It is the default for `build.rolldownOptions.input`, `build.lib.entry`, `build.ssr` (if `true`) and `optimizeDeps.entries` when those are unset. Useful with no `index.html`:

```js
export default defineConfig({
  input: 'src/main.ts',
})
```

## Checked

Date: 2026-11-07. Read shared-options.md (read in full) (`root`, `base`, `mode`, `input`). Removed the parenthetical about environments not inheriting `input`, which rests on a UI badge not explained in the page text. Everything else (defaults, base value forms, mode override and `--mode`, `input` defaults for `build.rolldownOptions.input`, `build.lib.entry`, `build.ssr` and `optimizeDeps.entries`) matched.

Method: documentation only; no commands were run.
