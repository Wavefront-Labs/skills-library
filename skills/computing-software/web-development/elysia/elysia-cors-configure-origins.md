---
id: computing-software.web-development.elysia.elysia-cors-configure-origins
name: elysia-cors-configure-origins
category: computing-software
field: web-development
product: elysia
tags: [cors, plugin, security, preflight]
level: practitioner
status: docs-checked
description: "Enable and tune CORS in Elysia with @elysia/cors: origin matching, methods, headers, credentials, preflight caching."
sources:
  - https://elysiajs.com/plugins/cors.html
  - https://elysiajs.com/integrations/better-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let browsers on chosen origins call your Elysia API.

1. Install: `bun add @elysia/cors`
2. Minimal use accepts any origin:

```typescript
import { Elysia } from 'elysia'
import { cors } from '@elysia/cors'

new Elysia().use(cors()).listen(3000)
```

3. Restrict it. Config options and defaults from the docs:
- `origin` (default `true`, which sets `Access-Control-Allow-Origin` to `*`). Accepts a string (assigned directly to the header), boolean, `RegExp` (matched against the request URL), a function `(context: Context) => boolean | void` (allowed when it returns `true`), or an array of any of those evaluated in order (allowed if any is true).
- `methods` (default `*`): `'*'`, a string such as `'GET, PUT, POST'`, or `string[]`; undefined/null/empty ignores all methods.
- `allowedHeaders` (default `*`): string or `string[]`, e.g. `['Content-Type', 'Authorization']`.
- `exposeHeaders` (default `*`): headers exposed to the browser.
- `credentials` (default `true`): sets `Access-Control-Allow-Credentials` (cookies, authorization headers, TLS client certs).
- `maxAge` (default `5`): how long a preflight result may be cached.
- `preflight`: whether the server answers OPTIONS preflight requests (those carry `Access-Control-Request-Method`, `Access-Control-Request-Headers`, `Origin`).

Allow every subdomain of one domain:

```typescript
new Elysia()
    .use(cors({ origin: /.*\.saltyaom\.com$/ }))
    .get('/', () => 'Hi')
    .listen(3000)
```

Pinned single origin with credentials, as used when fronting Better Auth:

```typescript
cors({
    origin: 'http://localhost:3001',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization']
})
```

Gotchas:
- Defaults are wide open (`origin: true`, `methods: *`); set `origin` explicitly in production.
- The Better Auth page registers `cors` before `.mount(auth.handler)`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/cors.html, integrations/better-auth.html); each claim, option name and default was compared with the page text. Removed the invented Verify step; reworded the Better Auth ordering gotcha to what that page shows.

Method: documentation only; no commands were run.
