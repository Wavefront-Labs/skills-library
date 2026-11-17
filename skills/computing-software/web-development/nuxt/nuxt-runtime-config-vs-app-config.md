---
id: computing-software.web-development.nuxt.nuxt-runtime-config-vs-app-config
name: nuxt-runtime-config-vs-app-config
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, app-config, runtime-config, defineappconfig, useappconfig]
level: practitioner
status: docs-checked
description: "Decide between runtimeConfig and app.config.ts using the docs comparison table, and define app.config with defineAppConfig and useAppConfig."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/03.configuration.md
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/3.app-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both expose variables to the rest of the app. The page's guidelines:

- `runtimeConfig`: private or public tokens that need to be specified after build using environment variables.
- `app.config`: public tokens determined at build time, website configuration such as theme variant or title, and any non-sensitive project config.

| Feature | runtimeConfig | app.config |
|---|---|---|
| Client-side | Hydrated | Bundled |
| Environment variables | Yes | No |
| Reactive | Yes | Yes |
| Types support | Partial | Yes |
| Configuration per request | No | Yes |
| Hot module replacement | No | Yes |
| Non-primitive JS types | No | Yes |

`app/app.config.ts` lives in the source directory (`srcDir`; it can be `.ts`, `.js` or `.mjs`) and exports `defineAppConfig`, which is globally available without import:

```ts
export default defineAppConfig({
  title: 'Hello Nuxt',
  theme: { dark: true, colors: { primary: '#ff0000' } },
})
```

Read it with `const appConfig = useAppConfig()`; it is available universally (server rendering and browser). `updateAppConfig(newConfig)` updates it at runtime. Do not put secret values in `app.config`: it is exposed to the client bundle. App config cannot be overridden with environment variables.

Known limitation (Nuxt v3.3 and later): `app.config.ts` is shared with Nitro, so you cannot import Vue components directly in it and some auto-imports are unavailable there.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/03.configuration.md and docs/2.directory-structure/1.app/3.app-config.md. Confirmed: guidelines, comparison table, defineAppConfig, useAppConfig, updateAppConfig, secrets warning, Nitro limitation. Removed: the unsupported "functions, class instances" gloss, the decision shortcut, and the invented Verify step.

Method: documentation only; no commands were run.
