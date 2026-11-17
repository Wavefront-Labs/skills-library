---
id: computing-software.web-development.hono.hono-jwt-middleware
name: hono-jwt-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, auth, jwt]
level: practitioner
status: docs-checked
description: "Protect Hono routes with the jwt middleware: secret, alg, cookie, headerName, realm, claim verification and reading jwtPayload."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/jwt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JWT auth middleware

Import: `import { jwt } from 'hono/jwt'` and `import type { JwtVariables } from 'hono/jwt'`.

It reads the token from the `Authorization` header (customise with `headerName`) unless the `cookie` option is set. The client header must include a scheme, e.g. `Bearer my.token.value`.

```ts
type Variables = JwtVariables // types c.get('jwtPayload')
const app = new Hono<{ Variables: Variables }>()

app.use('/auth/*', jwt({ secret: 'it-is-very-secret', alg: 'HS256' }))
app.get('/auth/page', (c) => c.text('You are authorized'))
```

Read the payload and verify claims:

```ts
app.use('/auth/*', jwt({
  secret: 'it-is-very-secret',
  alg: 'HS256',
  verification: { iss: 'my-trusted-issuer', aud: 'my-api' },
}))
app.get('/auth/page', (c) => c.json(c.get('jwtPayload')))
```

## Options
- `secret` (required, string) and `alg` (required): `HS256|HS384|HS512|RS256|RS384|RS512|PS256|PS384|PS512|ES256|ES384|ES512|EdDSA`.
- `cookie`: cookie name to read the token from.
- `headerName`: default `Authorization`, e.g. `'x-custom-auth-header'`.
- `realm`: for the `WWW-Authenticate` header on 401; default is the request URL.
- `verification`: `iss` (string|RegExp, not checked if unset), `aud` (string|string[]|RegExp; if set the token must have a matching `aud`), `nbf`, `iat`, `exp` (booleans, default true, checked if present).

## Using environment secrets
`jwt()` is just a function, so build it per request:

```js
app.use('/auth/*', (c, next) => {
  const jwtMiddleware = jwt({ secret: c.env.JWT_SECRET, alg: 'HS256' })
  return jwtMiddleware(c, next)
})
```

## Gotcha
`alg` is marked required. The Authorization header sent by the client must have a specified scheme (for example `Bearer my.token.value`).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/jwt.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); "omitting it fails" and "token is not accepted" (page says required / must have a scheme).

Method: documentation only; no commands were run.
