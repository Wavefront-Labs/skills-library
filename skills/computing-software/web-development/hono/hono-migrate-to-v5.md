---
id: computing-software.web-development.hono.hono-migrate-to-v5
name: hono-migrate-to-v5
category: computing-software
field: web-development
product: hono
tags: [hono, migration, v5, breaking-changes, upgrade]
level: advanced
status: docs-checked
description: "Upgrade a Hono v4 app to v5: ESM only, adapters moved to @hono packages, onError signature, typed query and json, removed APIs and wildcard rules."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/migrating-to-v5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating Hono v4 to v5

Try it: `npm install hono@next`.

- **ESM only.** Node.js 22.12+ required (`require('hono')` still works there).
- **Adapters are separate packages:** `hono/aws-lambda`, `hono/bun`, `hono/cloudflare-workers`, `hono/deno`, `hono/lambda-edge`, `hono/netlify`, `hono/service-worker`, `hono/vercel` become `@hono/<name>` (for example `import { serveStatic } from '@hono/bun'`). `hono/cloudflare-pages` is removed with no replacement (use Workers with static assets). `hono/adapter` (`env()`, `getRuntimeKey()`) stays.
- **`onError` is middleware-style:** `app.onError((c) => { console.error(c.error); return c.text('Custom Error', 500) })` instead of `(err, c)`. `notFound` accepts an optional path and several middleware; registrations compose, `next()` delegates, paths are independent of HTTP method and relative to `basePath()`.
- **Non-Error throws** go to `onError` wrapped in an Error; the original is `c.error.cause`.
- **Types:** `c.req.query()` returns `Record<string, string | undefined>`; `c.req.json()` returns `unknown`, so write `await c.req.json<{ name: string }>()` or use `c.req.valid()`.
- **`c.json(undefined)`** (or a function or symbol) now throws `TypeError`.
- **Wildcards:** a trailing `*` in a segment matches in every router (may match nothing); `/x*y` is not a wildcard; `/wild/*/card` does not match `/wild//card`. In RegExpRouter `/x*/y` and `/x/*` cannot coexist (UnsupportedPathError; SmartRouter falls back to TrieRouter).
- **Removed:** `getColorEnabledAsync()` (use `getColorEnabled(c.env)`); `app.mount()` (use `app.all('/itty-router/*', mount(handler))` from `hono/mount`); `app.fire()` (use `fire(app)` from `@hono/service-worker`); `c.req.matchedRoutes`/`c.req.routePath` (use `matchedRoutes()`/`routePath(c)` from `hono/route`); `getQueryStrings()`; `UnOfficalStatusCode` (use `UnofficialStatusCode`).
- **SSG:** `beforeRequestHook`, `afterResponseHook`, `afterGenerateHook` move into `toSSG(app, fs, { plugins: [{ beforeRequestHook }, defaultPlugin()] })`. `defaultPlugin()` applies only when `plugins` is omitted, so add it explicitly. `SSG_DISABLED_RESPONSE` becomes `X_HONO_DISABLE_SSG_HEADER_KEY`.
- **Bearer auth:** `noAuthenticationHeader.message`, `invalidAuthenticationHeader.message`, `invalidToken.message` replace the `*Message` options. `hashFunction` in Basic/Bearer auth is typed `(input: string) => string | null | Promise<string | null>`; `serveStatic` drops `pathResolve`.

## Gotcha
`c.req.json()` now returns `unknown` and `c.req.query()` values may be `undefined`, so code that relied on `any` or `string` needs explicit types or `c.req.valid()`.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page guides/migrating-to-v5.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
