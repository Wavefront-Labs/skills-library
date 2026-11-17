---
id: computing-software.web-development.nuxt.nuxt-runtime-config-env-vars
name: nuxt-runtime-config-env-vars
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, runtime-config, environment-variables, secrets, dotenv]
level: practitioner
status: docs-checked
description: "Expose private and public values with runtimeConfig, override them with NUXT_ prefixed environment variables, and read them through useRuntimeConfig."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/03.configuration.md
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/6.going-further/10.runtime-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`runtimeConfig` exposes values such as environment variables to the app. Keys are server-side only by default; keys inside `runtimeConfig.public` and `runtimeConfig.app` (used by Nuxt internally) are also available client-side. Define values in `nuxt.config`, then override them with environment variables.

```ts
export default defineNuxtConfig({
  runtimeConfig: {
    // private, server only
    apiSecret: '123',
    public: {
      apiBase: '/api',
    },
  },
})
```

```ini
# .env overrides apiSecret
NUXT_API_SECRET=api_secret_token
NUXT_PUBLIC_API_BASE=https://nuxtjs.org
```

Two requirements from the page: custom runtime config variables must be defined in `nuxt.config` (so arbitrary environment variables are not exposed), and only an uppercase variable starting with `NUXT_`, using `_` to separate keys and case changes, can override a property. So `apiSecret` is `NUXT_API_SECRET` and `public.apiBase` is `NUXT_PUBLIC_API_BASE`.

Gotchas stated on the page:
- The Nuxt CLI reads `.env` in development, build and generate, but a built server does not read your `.env` file.
- Defaulting a value to a differently named variable (for example `process.env.OTHER_VARIABLE`) works only at build time and breaks at runtime.
- Values are cast with `destr`: `NUXT_MY_VAR=4848e0` becomes the number 4848. To keep a string, the value itself must contain literal double quotes (`NUXT_MY_VAR='"4848e0"'` in `.env`).
- Runtime config is serialised before it reaches Nitro, so functions, Sets and Maps should not be set in `nuxt.config`.

Reading: call `useRuntimeConfig()` in the Vue app, plugins (inside `defineNuxtPlugin`) and server routes. On the client only `public` and `app` keys exist, and the object is writable and reactive; on the server the whole config is available but read-only. Do not expose runtime config keys to the client by rendering them or passing them to `useState`. Public values are also available in templates as `$config.public`.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/03.configuration.md and docs/3.guide/6.going-further/10.runtime-config.md. Confirmed: key visibility, the two override requirements, NUXT_ mapping, reading rules. Added the page's gotchas. Removed: the unsupported rules "secrets never under public" and the app.config cross-reference, and the invented Verify step.

Method: documentation only; no commands were run.
