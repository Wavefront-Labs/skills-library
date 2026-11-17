---
id: computing-software.web-development.vite.env-dir-prefix-apptype
name: env-dir-prefix-apptype
category: computing-software
field: web-development
product: vite
tags: [env-dir, env-prefix, app-type, expose-unprefixed-env]
level: practitioner
status: docs-checked
description: "Set envDir and envPrefix (never an empty string; expose single variables via define) and choose appType spa, mpa or custom."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`envDir` (`string | false`, default `root`): where `.env` files load from; absolute or relative to the root. `false` disables env file loading.

`envPrefix` (`string | string[]`, default `VITE_`): variables with this prefix are exposed via `import.meta.env`. Never set it to `''`; that would expose all variables and Vite throws. To expose one unprefixed variable use `define`:

```js
define: {
  'import.meta.env.ENV_VARIABLE': JSON.stringify(process.env.ENV_VARIABLE)
}
```

`appType` (`'spa' | 'mpa' | 'custom'`, default `'spa'`):
- `'spa'`: HTML middlewares plus SPA fallback; preview configures sirv with `single: true`.
- `'mpa'`: HTML middlewares only.
- `'custom'`: no HTML middlewares (SSR and frameworks with custom HTML handling).

Related: `server.middlewareMode`.

## Checked

2026-11-07. Confirmed against the `envDir`, `envPrefix` and `appType` sections of config/shared-options.md (the page was fetched in full; the other long sections were skimmed, these three were read line by line): types and defaults, the `''` prefix warning with Vite throwing, the `define` workaround snippet, and the three `appType` meanings including sirv `single: true` in preview. Nothing removed.

Method: documentation only; no commands were run.
