---
id: computing-software.web-development.vite.env-variables-vite-prefix
name: env-variables-vite-prefix
category: computing-software
field: web-development
product: vite
tags: [import-meta-env, vite-prefix, built-in-constants, env-secrets]
level: intro
status: docs-checked
description: "Use import.meta.env: built-in MODE, BASE_URL, PROD, DEV, SSR constants, the VITE_ prefix exposure rule, string-typed values, and why not to put secrets there."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Constants are globals in dev and statically replaced at build, so branches like `if (import.meta.env.DEV)` are tree-shaken in production.

Built-ins, always available:
- `MODE`: the mode (string)
- `BASE_URL`: from the `base` option
- `PROD`: true when `NODE_ENV='production'`
- `DEV`: always the opposite of `PROD`
- `SSR`: true when running on the server

Only variables prefixed `VITE_` are exposed to client code (change via `envPrefix`):

```
VITE_SOME_KEY=123
DB_PASSWORD=foobar
```

```js
console.log(import.meta.env.VITE_SOME_KEY) // "123"
console.log(import.meta.env.DB_PASSWORD) // undefined
```

Values are always strings, including numbers and booleans; convert them yourself.

Never put API keys or other secrets in `VITE_*` variables: they are bundled into your source at build time. Use a backend or serverless/edge function.

## Checked

2026-11-04. Confirmed against the Vite Env Variables and Modes guide (docs/guide/env-and-mode.md): built-in constants, VITE_ prefix rule, string values, secrets warning. Nothing removed.

Method: documentation only; no commands were run.
