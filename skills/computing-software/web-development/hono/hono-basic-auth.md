---
id: computing-software.web-development.hono.hono-basic-auth
name: hono-basic-auth
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, auth, basic-auth]
level: practitioner
status: docs-checked
description: "Protect Hono routes with HTTP Basic authentication using the basicAuth middleware, including multiple users, verifyUser and onAuthSuccess."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/basic-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Basic auth in Hono

Import: `import { basicAuth } from 'hono/basic-auth'`.

Apply to a path pattern:

```ts
app.use(
  '/auth/*',
  basicAuth({ username: 'hono', password: 'acoolproject' })
)
app.get('/auth/page', (c) => c.text('You are authorized'))
```

Restrict one route and method by putting it before the handler: `app.delete('/auth/page', basicAuth({ username: 'hono', password: 'acoolproject' }), (c) => c.text('Page deleted'))`.

## Options
- `username` and `password` are marked required; the page's `verifyUser` example passes only `verifyUser`.
- `realm`: used in the `WWW-Authenticate` challenge, default `"Secure Area"`.
- `hashFunction`: handles hashing for safe comparison of passwords.
- `verifyUser(username, password, c)`: return `true` (or a Promise of it) to accept. Use it to check dynamic users.
- `invalidUserMessage`: string, object or `(c) => string | object | Promise`.
- `onAuthSuccess(c, username)`: runs after success so you can `c.set('username', username)` without re-parsing the Authorization header.

## Multiple users
Pass extra objects as further arguments. Only the first object may carry other options such as `realm`:

```ts
basicAuth(
  { username: 'hono', password: 'acoolproject', realm: 'www.example.com' },
  { username: 'hono-admin', password: 'super-secure' }
)
```

Or spread from config: `basicAuth({ realm: 'www.example.com', ...users[0] }, ...users.slice(1))`.

## Gotcha
In the extra user objects you cannot redefine `realm` or other params; they are read only from the first object.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/basic-auth.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the unstated "required unless verifyUser" rule (reworded to what the page shows).

Method: documentation only; no commands were run.
