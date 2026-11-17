---
id: computing-software.web-development.elysia.elysia-jwt-sign-verify-cookie-or-header
name: elysia-jwt-sign-verify-cookie-or-header
category: computing-software
field: web-development
product: elysia
tags: [jwt, authentication, plugin, cookie, jose]
level: practitioner
status: docs-checked
description: "Sign and verify JSON Web Tokens in Elysia handlers with @elysia/jwt, storing the token in a cookie or reading it from a header."
sources:
  - https://elysiajs.com/plugins/jwt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: issue a JWT at sign-in and check it on protected routes.

1. Install: `bun add @elysia/jwt`
2. Register with a secret (load it from the environment, not source):

```typescript
import { Elysia } from 'elysia'
import { jwt } from '@elysia/jwt'

const app = new Elysia()
    .use(jwt({ name: 'jwt', secret: process.env.JWT_SECRETS! }))
```

3. Cookie flow:

```typescript
.get('/sign/:name', async ({ jwt, params: { name }, cookie: { auth } }) => {
    const value = await jwt.sign({ name })
    auth.set({ value, httpOnly: true, maxAge: 7 * 86400, path: '/profile' })
    return `Sign in as ${value}`
})
.get('/profile', async ({ jwt, status, cookie: { auth } }) => {
    const profile = await jwt.verify(auth.value)
    if (!profile) return status(401, 'Unauthorized')
    return `Hello ${profile.name}`
})
```

4. Header flow: `jwt.verify(authorization)` using `headers: { authorization }`.

Handler API:
- `jwt.sign(payload): Promise<string>`; payload accepts the claim fields from the config (iss, sub, aud, jti, nbf, exp, iat).
- `jwt.verify(token: string): Promise<payload | false>`. A falsy result means invalid, so always branch on it.

Gotchas:
- The docs' header example destructures `error` but then calls `status(401, ...)`; destructure `status` as in the cookie example or the call fails.
- The `name` option sets the context property: `name: 'myJWTNamespace'` gives `({ myJWTNamespace })`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/jwt.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the Bearer-prefix inference that the page does not state.

Method: documentation only; no commands were run.
