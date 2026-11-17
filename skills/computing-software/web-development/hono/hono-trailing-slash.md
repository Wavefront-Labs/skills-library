---
id: computing-software.web-development.hono.hono-trailing-slash
name: hono-trailing-slash
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, routing, redirect]
level: practitioner
status: docs-checked
description: "Normalize trailing slashes in Hono with appendTrailingSlash and trimTrailingSlash, including alwaysRedirect and skip options."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/trailing-slash.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trailing slash

Import: `import { appendTrailingSlash, trimTrailingSlash } from 'hono/trailing-slash'`.

Redirect `/about/me` to `/about/me/`:

```ts
const app = new Hono({ strict: true })
app.use(appendTrailingSlash())
app.get('/about/me/', (c) => c.text('With Trailing Slash'))
```

Redirect `/about/me/` to `/about/me`:

```ts
const app = new Hono({ strict: true })
app.use(trimTrailingSlash())
app.get('/about/me', (c) => c.text('Without Trailing Slash'))
```

## Options (both functions)
- `alwaysRedirect: boolean`: by default redirect only happens when the response status is 404. With `true` it redirects before handlers run, which is needed for wildcard routes:

```ts
app.use(trimTrailingSlash({ alwaysRedirect: true }))
app.get('/my-path/*', (c) => c.text('Wildcard route'))
```

- `skip: (path) => boolean`: return true to skip the redirect, e.g. for file extensions:

```ts
app.use(appendTrailingSlash({ skip: (path) => /\.\w+$/.test(path) }))
```

## Gotcha
It only applies to GET requests whose response is 404 (unless `alwaysRedirect`). Wildcard routes match before 404, so the default does nothing there.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/trailing-slash.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
