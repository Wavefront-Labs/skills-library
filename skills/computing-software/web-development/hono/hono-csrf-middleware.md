---
id: computing-software.web-development.hono.hono-csrf-middleware
name: hono-csrf-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, csrf, security]
level: practitioner
status: docs-checked
description: "Defend Hono apps against CSRF using the csrf middleware that checks Origin and Sec-Fetch-Site, with static and dynamic validation options."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/csrf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CSRF protection

Import: `import { csrf } from 'hono/csrf'`.

It checks the `Origin` header and the `Sec-Fetch-Site` header; the request is allowed if EITHER validation passes. It only validates unsafe methods (not GET, HEAD, OPTIONS) with form-sendable content types: `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`.

```ts
app.use(csrf()) // default: same origin / same-origin only
app.use(csrf({ origin: 'https://myapp.example.com' }))
app.use(csrf({ origin: ['https://myapp.example.com', 'https://development.myapp.example.com'] }))
app.use(csrf({ secFetchSite: 'same-origin' }))
app.use(csrf({ secFetchSite: ['same-origin', 'none'] }))
```

## Options
- `origin`: string, string[] or `(origin, c) => boolean`. Default: same origin as the request URL.
- `secFetchSite`: string, string[] or `(secFetchSite, c) => boolean`. Default: only `'same-origin'`. Values: `same-origin`, `same-site`, `cross-site`, `none`.

## Dynamic examples
```ts
app.use('*', csrf({ origin: (origin) => /https:\/\/(\w+\.)?myapp\.example\.com$/.test(origin) }))

app.use(csrf({
  secFetchSite: (secFetchSite, c) => {
    if (secFetchSite === 'same-origin') return true
    if (secFetchSite === 'cross-site' && c.req.path.startsWith('/webhook/')) return true
    return false
  },
}))
```

## Gotchas
- Anchor regexes with `$`; never do a forward (prefix) match.
- Old browsers that omit `Origin`, or reverse proxies that strip the headers, may break; use token-based CSRF there.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/csrf.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
