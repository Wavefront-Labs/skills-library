---
id: computing-software.web-development.vite.config-define-plugins-dirs
name: config-define-plugins-dirs
category: computing-software
field: web-development
product: vite
tags: [define-option, plugins-option, public-dir-option, cache-dir]
level: practitioner
status: docs-checked
description: "Options define (Oxc global replacement, JSON-serializable values), plugins (falsy and promises), publicDir (false to disable) and cacheDir (default node_modules/.vite)."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`define`: global constants, defined as globals in dev and statically replaced in build via Oxc's define. Values must be a string containing a JSON-serializable value or a single identifier; non-strings are run through `JSON.stringify`.

```js
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify('v1.0.0'),
    __API_URL__: 'window.__backend_api_url',
  },
})
```

For TypeScript declare them, such as `declare const __APP_VERSION__: string` in `vite-env.d.ts`.

`plugins`: `(Plugin | Plugin[] | Promise<Plugin | Plugin[]>)[]`; falsy entries are ignored, arrays flattened, promises resolved first.

`publicDir`: `string | false`, default `"public"`. Served at `/` in dev and copied to `outDir` root, always as-is without transform. `false` disables the feature.

`cacheDir`: default `"node_modules/.vite"` (`.vite` when no `package.json` is found). Holds pre-bundled deps and other caches; regenerate with `--force` or by deleting it.

## Checked

Date: 2026-11-07. Read shared-options.md (read in full) (`define`, `plugins`, `publicDir`, `cacheDir`). Oxc-based replacement, JSON-serializable value rule, falsy/array/promise plugin handling, `publicDir` default `"public"` and `false`, `cacheDir` default and `.vite` fallback all matched; nothing trimmed.

Method: documentation only; no commands were run.
