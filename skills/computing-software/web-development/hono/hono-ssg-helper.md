---
id: computing-software.web-development.hono.hono-ssg-helper
name: hono-ssg-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, ssg, static-site, plugins]
level: advanced
status: docs-checked
description: "Generate a static site from a Hono app with toSSG: options, file naming, ssgParams, isSSGContext, disableSSG, onlySSG and plugins."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/ssg.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSG helper

Import: `import { toSSG, defaultExtensionMap, defaultPlugin, redirectPlugin } from 'hono/ssg'`.

```ts
// build.ts (Node.js)
import app from './index'
import { toSSG } from 'hono/ssg'
import fs from 'fs/promises'
toSSG(app, fs)
```
Outputs `./static/index.html` and `./static/about.html`. On Deno/Bun use `toSSG` from `@hono/deno` / `@hono/bun` (`toSSG(app)`). A Vite plugin exists: `@hono/vite-ssg`.

## Options (ToSSGOptions)
`dir` (default `./static`), `concurrency` (default `2`), `extensionMap` (Content-Type to extension; spread `...defaultExtensionMap`), `plugins`. Returns `{ success, files, error? }`.

## File naming
`/` to `index.html`; `/path` to `path.html`; `/path/` to `path/index.html`. Extension follows Content-Type (`c.html` gives `.html`); a trailing slash always gives `index.ext`.

## Middleware
- `ssgParams(async () => shops.map(s => ({ id: s.id })))` before a dynamic route like `/shops/:id` (like Next.js generateStaticParams).
- `isSSGContext(c)` true during `toSSG`.
- `disableSSG()` excludes a route; `onlySSG()` makes it return `c.notFound()` after `toSSG` has run.

## Plugins
Hooks: `beforeRequestHook(req)` (return `false` to skip), `afterResponseHook(res)` (return `false` to skip file), `afterGenerateHook(result)`. `defaultPlugin()` skips non-200 responses and is used only if you pass no plugins; to keep it add it explicitly. `redirectPlugin()` writes HTML meta-refresh pages for 301/302/303/307/308 and must come BEFORE `defaultPlugin()`:

```ts
toSSG(app, fs, { plugins: [redirectPlugin(), defaultPlugin()] })
```

## Gotcha
Custom plugins replace the default one, so non-200 files may be generated unless you re-add `defaultPlugin()`.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/ssg.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
