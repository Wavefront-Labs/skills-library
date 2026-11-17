---
id: computing-software.web-development.vite.environment-app-build
name: environment-app-build
category: computing-software
field: web-development
product: vite
tags: [builder-option, build-app-hook, create-builder, vite-build-app]
level: advanced
status: docs-checked
description: "Build every environment with the builder option, builder.buildApp ordering with the buildApp hook, parallel builds, createBuilder and vite build --app."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-frameworks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vite build` and `vite build --ssr` still build only the client or only ssr environment. When the `builder` option is set (even `{}`, as `vite build --app` does), `vite build` builds the whole app via a `ViteBuilder`; this becomes the default in a future major. Environments build in series, in `environments` record order.

Control it with `builder.buildApp`, for example parallel builds:

```js
export default defineConfig({
  builder: {
    buildApp: async (builder) => {
      const environments = Object.values(builder.environments)
      await Promise.all(environments.map((environment) => builder.build(environment)))
    },
  },
})
```

The `buildApp` plugin hook (global, async, sequential, `(builder) => Promise<void>`) also participates. Order: hooks with `order` `'pre'` or `null`, then the configured `builder.buildApp`, then `'post'` hooks. `environment.isBuilt` tells whether an environment was built already.

Programmatically use `createBuilder`, the build-time equivalent of `createServer`:

```js
import { createBuilder } from 'vite'
const builder = await createBuilder()
await builder.buildApp()   // same as vite build --app
```

`builder.build(environment)` builds one. The standalone `build` handles only the legacy client-only and ssr-only builds.

## Checked

2026-11-07. Confirmed against the "Environments During Build" section of guide/api-environment-frameworks.md (page read in full): `vite build` and `vite build --ssr` behaviour, the `builder` option (even `{}`, as `vite build --app` does), series order, the `builder.buildApp` parallel example, the `buildApp` plugin hook kind and ordering (`pre` or `null`, then the config option, then `post`), `environment.isBuilt`, `createBuilder` and `builder.build(environment)`. Nothing removed.

Method: documentation only; no commands were run.
