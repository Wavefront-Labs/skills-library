---
id: computing-software.devops-ci-cd.build-systems.embedding-version-in-js-bundles
name: embedding-version-in-js-bundles
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, vite-define, build-metadata, import-meta-env, webpack-defineplugin, git-sha, sentry-release]
level: practitioner
status: docs-checked
description: "Embed version, git SHA and build time into JavaScript bundles with Vite define and import.meta.env, webpack DefinePlugin and Next.js, and wire it to error tracking releases."
sources: ["https://vite.dev/config/shared-options.html#define", "https://vite.dev/guide/env-and-mode", "https://webpack.js.org/plugins/define-plugin/", "https://docs.sentry.io/platforms/javascript/configuration/releases/", "https://docs.sentry.io/product/releases/naming-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Embedding version in JS bundles

Knowing exactly which build a browser is running is essential for support, error tracking and cache debugging.

## Vite
```ts
// vite.config.ts
import { defineConfig } from 'vite'
import { execSync } from 'node:child_process'
import { readFileSync } from 'node:fs'

const pkg = JSON.parse(readFileSync('./package.json', 'utf8'))
const sha = process.env.GITHUB_SHA ?? execSync('git rev-parse HEAD').toString().trim()

export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(pkg.version),
    __GIT_SHA__: JSON.stringify(sha.slice(0, 12)),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
  },
})
```
```ts
// src/env.d.ts
declare const __APP_VERSION__: string
declare const __GIT_SHA__: string
declare const __BUILD_TIME__: string
```
- `define` entries are global constant replacements: during build they are statically replaced. A string value is used as a code expression, so wrap strings with `JSON.stringify` (non-string values are stringified by Vite).
- Alternative: env vars prefixed `VITE_` (`VITE_GIT_SHA=$GITHUB_SHA vite build`) read as `import.meta.env.VITE_GIT_SHA`. Only `VITE_*` variables are exposed to client code; never put secrets there - everything ends up in the public bundle.

## webpack / Next.js
```js
new webpack.DefinePlugin({ __GIT_SHA__: JSON.stringify(process.env.GIT_SHA) })
// Next.js: env vars prefixed NEXT_PUBLIC_ are inlined into the browser bundle at build time
```
webpack's DefinePlugin replaces variables at compile time; string values are used as code fragments, hence `JSON.stringify`.

## Expose it
- Console banner or `window.__BUILD__ = { version, sha }` for support.
- A `/version.json` emitted at build time (also lets the app detect "new version available" by polling it).
- HTML: Vite replaces `%CONST_NAME%` for any `import.meta.env` property in HTML files, e.g. `<meta name="app-version" content="%VITE_APP_VERSION%">` when `VITE_APP_VERSION` is set.

## Error tracking
```ts
Sentry.init({ dsn, release: `web@${__APP_VERSION__}+${__GIT_SHA__}` })
```
Sentry recommends release names of the form `package@version` or `package@version+build` (or a commit SHA); names cannot contain newlines, tabs or slashes and are limited to 200 characters. Upload source maps for the same release in CI with `sentry-cli sourcemaps upload` or `@sentry/vite-plugin`, so stack traces map to the deployed code.

## Caching consequence
A `__BUILD_TIME__` value that changes on every build changes the content of whatever chunk uses it, which changes that chunk's hash and defeats long-term caching. Keep build metadata in a small separate module or in `version.json`, and omit build time if you want reproducible bundles.

## Verify
- [ ] The production bundle contains the commit SHA (search `dist/` for the 12-character SHA) and the UI/about page shows it.
- [ ] Sentry events carry the release matching the deployed commit.

## Checked
Date: 2026-10-25. Documentation: Vite docs (vitejs/vite `docs/config/shared-options.md`, `docs/guide/env-and-mode.md`), webpack DefinePlugin page (webpack/webpack.js.org), Next.js environment-variables guide (vercel/next.js), Sentry docs (getsentry/sentry-docs: releases, naming releases, Vite plugin, CLI source maps).
Confirmed: Vite `define` static replacement and string-as-expression behaviour; `VITE_` prefix exposure; `%CONST_NAME%` HTML replacement; DefinePlugin semantics; `NEXT_PUBLIC_` inlining; Sentry release naming format and restrictions; `sentry-cli sourcemaps upload` and `@sentry/vite-plugin`.
Removed: the esbuild `define` example (no esbuild documentation was read), the `package.json` import with a JSON import attribute (replaced by a plain `readFileSync`), and `sentry-cli ... --release` flag details (not in the pages read).
Method: documentation only; no commands were run.
