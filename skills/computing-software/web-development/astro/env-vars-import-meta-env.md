---
id: computing-software.web-development.astro.env-vars-import-meta-env
name: env-vars-import-meta-env
category: computing-software
field: web-development
product: astro
tags: [environment-variables, import-meta-env, public-prefix, env-files, loadenv]
level: intro
status: docs-checked
description: "Use environment variables in Astro with import.meta.env: the PUBLIC_ prefix rule, built-in MODE/PROD/DEV/BASE_URL/SITE, .env mode files, and config-file loading."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro uses Vite's env support: values are statically replaced at build time. All variables are available in server-side code, but only those prefixed `PUBLIC_` reach client-side code.

```ini title=".env"
SECRET_PASSWORD=password123
PUBLIC_ANYBODY=there
```

Access with `import.meta.env.PUBLIC_ANYBODY` (not `process.env`). Built-ins: `MODE` (`development` for `astro dev`, `production` for `astro build`), `PROD`, `DEV`, `BASE_URL` (from `base`), `SITE` (from `site`).

Mode-specific files such as `.env.testing` or `.env.staging` load via the `--mode` flag:

```shell
pnpm astro dev --mode staging
pnpm astro build --mode testing
```

TypeScript IntelliSense for custom variables:

```ts title="src/env.d.ts"
interface ImportMetaEnv {
  readonly DB_PASSWORD: string;
  readonly PUBLIC_POKEAPI: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

`.env` files are not loaded inside configuration files, because config is evaluated first. Use `process.env` there, or Vite's `loadEnv`:

```js title="astro.config.mjs"
import { loadEnv } from "vite";

const { SECRET_PASSWORD } = loadEnv(process.env.NODE_ENV, process.cwd(), "");
```

With pnpm you need to install `vite` to use `loadEnv`. In SSR, runtime access depends on the adapter: usually `process.env`, `Deno.env.get()` for Deno; Astro checks the server environment first, then `.env` files.

## Checked

2026-11-04. Confirmed against the Astro environment variables guide: PUBLIC_ prefix rule, built-in MODE/PROD/DEV/BASE_URL/SITE, --mode with env files, env.d.ts typing, loadEnv and adapter runtime access. Nothing removed.

Method: documentation only; no commands were run.
