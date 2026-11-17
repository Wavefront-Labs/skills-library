---
id: computing-software.web-development.vite.config-load-env
name: config-load-env
category: computing-software
field: web-development
product: vite
tags: [load-env, env-in-config, define-app-constant]
level: practitioner
status: docs-checked
description: "Use .env values inside vite.config with loadEnv, because env files load only after the config resolves; empty prefix loads everything."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
While the config is evaluated, only variables already in `process.env` exist. Vite defers `.env*` loading until after the user config resolves because the files depend on `root`, `envDir` and the final `mode`. So values in `.env`, `.env.local`, `.env.[mode]` and `.env.[mode].local` are not in `process.env` during the config; they reach app code later via `import.meta.env` (with the `VITE_` prefix filter). If you only pass values to the app, call nothing.

When `.env*` values must shape the config itself, load them with `loadEnv`:

```js
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  // Third parameter '' loads all env regardless of the VITE_ prefix.
  const env = loadEnv(mode, process.cwd(), '')
  return {
    define: { __APP_ENV__: JSON.stringify(env.APP_ENV) },
    server: { port: env.APP_PORT ? Number(env.APP_PORT) : 5173 },
  }
})
```

## Checked

2026-11-04. Confirmed against the Vite config guide (docs/config/index.md, Using Environment Variables in Config): deferred .env loading, loadEnv with an empty third argument, example code. Nothing removed.

Method: documentation only; no commands were run.
