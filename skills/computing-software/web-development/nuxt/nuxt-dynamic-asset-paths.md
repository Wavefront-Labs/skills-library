---
id: computing-software.web-development.nuxt.nuxt-dynamic-asset-paths
name: nuxt-dynamic-asset-paths
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, assets, dynamic-import, import-meta-glob, base-url]
level: practitioner
status: docs-checked
description: "Handle assets whose path is built at runtime: public URLs with baseURL, Vite dynamic imports and import.meta.glob, with SSR cautions."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/05.assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a `src` is a static string literal, the build tool rewrites it: a public path such as `/img/nuxt.png` gets `app.baseURL` applied at runtime, and a bundled path such as `~/assets/img/nuxt.png` becomes an import resolving to the hashed output file. A bound `:src` assembled at runtime is opaque to the build tool and used exactly as written: `<img :src="`~/assets/img/${name}.png`">` does not work because Vite never sees it as an import, and a runtime-built public path like `/img/${name}.png` is not prefixed with `app.baseURL`. If the app is deployed below the origin root, prefix it yourself with `useRuntimeConfig().app.baseURL` (for example via `joinURL` from ufo).

Options from the docs:

1. Public assets: put files that need no processing or hashing in `public/` and build the URL, for example `computed(() => `/img/${props.name}.png`)`. Files in `public/` keep their original filenames.
2. Known set of files (Vite): list explicit imports with literal paths, loading only the selected module at runtime.

```ts
const logos = {
  light: () => import('./assets/img/logo-light.png?url'),
  dark: () => import('./assets/img/logo-dark.png?url'),
}
const logoUrl = (await logos[props.theme]()).default
```

3. Variable dynamic import: only the filename is dynamic; keeping the directory and extension in the import lets Vite find the possible files at build time: ``(await import(`./assets/img/${name}.png?url`)).default``.
4. `import.meta.glob` with `{ query: '?url', import: 'default' }` for a broader pattern or an explicit map of available files (the docs' example throws an error when the key is missing from the map). Glob imports are lazy by default; add `eager: true` if the URLs must be available synchronously. Every matching asset is still included in the build output; an eager glob loads all matches up front and can increase the initial JavaScript size or inline small assets.

Warning from the docs: await a lazy import before using its URL in server-rendered markup. Vite's `new URL(..., import.meta.url)` pattern does not work with SSR.

## Checked

2026-11-04. Confirmed against the Nuxt assets page: static versus dynamic src rewriting, baseURL handling, the public, explicit import, variable import and import.meta.glob options, eager behaviour, the SSR warning. Removed the Verify step.

Method: documentation only; no commands were run.
