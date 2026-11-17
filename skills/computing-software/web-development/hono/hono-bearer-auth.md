---
id: computing-software.web-development.hono.hono-bearer-auth
name: hono-bearer-auth
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, auth, bearer-auth, tokens]
level: practitioner
status: docs-checked
description: "Verify API tokens from the Authorization header with Hono bearerAuth, including multiple tokens, verifyToken and custom error responses."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/bearer-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bearer auth in Hono

Import: `import { bearerAuth } from 'hono/bearer-auth'`. Clients send `Authorization: Bearer {token}`.

```ts
const token = 'honoiscool'
app.use('/api/*', bearerAuth({ token }))
app.get('/api/page', (c) => c.json({ message: 'You are authorized' }))
```

Per route and method: `app.post('/api/page', bearerAuth({ token }), (c) => c.json({ message: 'Created post!' }, 201))`.

## Different tokens per method
`token` accepts `string | string[]`. To let a read token read but only a privileged token write, call `bearerAuth` inside `app.on`:

```ts
const privilegedMethods = ['POST', 'PUT', 'PATCH', 'DELETE']
app.on('GET', '/api/page/*', async (c, next) => {
  const bearer = bearerAuth({ token: [readToken, privilegedToken] })
  return bearer(c, next)
})
app.on(privilegedMethods, '/api/page/*', async (c, next) => {
  const bearer = bearerAuth({ token: privilegedToken })
  return bearer(c, next)
})
```

## Options
- `token` (marked required; the page's `verifyToken` example passes only `verifyToken`), `realm` (default `""`), `prefix` (default `"Bearer"`), `headerName` (default `Authorization`), `hashFunction`.
- `verifyToken: async (token, c) => token === 'dynamic-token'` returns true to accept.
- `noAuthenticationHeader`, `invalidAuthenticationHeader`, `invalidToken`: each an object with `wwwAuthenticateHeader` and `message` (string, object or `(c) => ...`).

## Gotcha
The token must match `/[A-Za-z0-9._~+/-]+=*/` or the middleware returns a 400. It need not be a JWT.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/bearer-auth.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the unstated "required unless verifyToken" rule (reworded to what the page shows).

Method: documentation only; no commands were run.
