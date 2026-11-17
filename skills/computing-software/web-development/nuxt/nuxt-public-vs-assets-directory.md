---
id: computing-software.web-development.nuxt.nuxt-public-vs-assets-directory
name: nuxt-public-vs-assets-directory
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, assets, public-directory, vite, static-files]
level: intro
status: docs-checked
description: "Choose between public/ (served as-is at root) and app/assets/ (processed by the build tool) and reference each correctly."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/05.assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt uses two directories for assets such as stylesheets, fonts or images.

- `public/` content is served at the server root as-is. A file `public/img/nuxt.png` is available at `/img/nuxt.png`, and templates reference it by that URL: `<img src="/img/nuxt.png">`. Files there keep their original filenames.
- `app/assets/` holds, by convention, every asset you want the build tool (Vite, the default, or webpack) to process, for example stylesheets, fonts and SVGs; this transforms files mainly for performance or caching (minification, cache invalidation). There is no auto-scan of this directory and you can use any other name. Reference files with the `~/assets/` path: `<img src="~/assets/img/nuxt.png">`.

Nuxt does not serve `app/assets/` at a static URL like `/assets/my-file.png`. If you need a static URL, use `public/`.

Static vs dynamic `src`: when `src` is a static string literal, the build tool rewrites it into a helper that resolves the final URL. A public path is wrapped so `app.baseURL` is applied at render time (so it works even if the base URL is only known at deploy time, for example via `NUXT_APP_BASE_URL`), and a bundled path additionally becomes an import resolving to the hashed output file. A bound `:src` assembled at runtime is opaque to the build tool: the string is used as written, so `` :src="`~/assets/img/${name}.png`" `` does not work and a runtime-built public path is not prefixed with `app.baseURL` (prefix it yourself with `useRuntimeConfig().app.baseURL`, for example via `joinURL`).

For runtime-chosen files, either put them in `public/` and reference by URL, or with Vite use explicit `import('./assets/img/logo-light.png?url')` imports, a variable dynamic import with only the filename dynamic, or `import.meta.glob` (lazy by default; `eager: true` loads all matches up front). Await a lazy import before using its URL in server-rendered markup; Vite's `new URL(..., import.meta.url)` pattern does not work with SSR.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/05.assets.md. Confirmed: directory roles, URL behaviour, baseURL handling, dynamic-path options. Removed: the unsupported use cases (robots.txt, favicons, emails), the rule of thumb, and the invented Verify step (build output check).

Method: documentation only; no commands were run.
