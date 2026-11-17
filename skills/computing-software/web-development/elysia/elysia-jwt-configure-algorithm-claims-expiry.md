---
id: computing-software.web-development.elysia.elysia-jwt-configure-algorithm-claims-expiry
name: elysia-jwt-configure-algorithm-claims-expiry
category: computing-software
field: web-development
product: elysia
tags: [jwt, jose, claims, plugin, authentication]
level: advanced
status: docs-checked
description: "Configure @elysia/jwt for multiple namespaces, signing algorithm, standard claims, expiry and strict payload schema."
sources:
  - https://elysiajs.com/plugins/jwt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: harden and customise JWT issuing beyond the defaults.

`@elysia/jwt` extends the options of the `jose` library. Install: `bun add @elysia/jwt`.

Options:
- `name`: the context key the `jwt` object is registered under. Use distinct names to register several JWT configs on one server (for example an access and a refresh config), each with its own `secret`.
- `secret`: the key used to sign the payload.
- `schema`: strict type validation of the JWT payload.
- `alg` (default `HS256`): one of HS256, HS384, HS512, PS256, PS384, PS512, RS256, RS384, RS512, ES256, ES256K, ES384, ES512, EdDSA.
- Registered claims: `iss` (issuer), `sub` (subject), `aud` (audience), `jti` (unique id), `nbf` (not before), `exp` (expiration), `iat` (issued at).
- JWS header parameters: `b64`, `kid`, `x5t`, `x5c`, `x5u`, `jwk`, `typ`, `ctr`.

Set an expiry with `exp`:

```typescript
const app = new Elysia()
    .use(jwt({ name: 'jwt', secret: process.env.JWT_SECRETS!, exp: '7d' }))
    .get('/sign/:name', async ({ jwt, params }) => jwt.sign(params))
```

This signs tokens that expire in 7 days.

Two namespaces:

```typescript
new Elysia()
    .use(jwt({ name: 'accessJwt', secret: process.env.ACCESS_SECRET!, exp: '15m' }))
    .use(jwt({ name: 'refreshJwt', secret: process.env.REFRESH_SECRET!, exp: '7d' }))
```

The two-namespace example is illustrative: it combines the documented options `name`, `secret` and `exp`; the docs only state that several names can be registered.

Gotchas:
- `verify` resolves to `false` (not a throw) on failure.
- The docs' `name` example reads the secret from `process.env.JWT_SECRETS`; the other samples inline a string.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/jwt.html); each claim, option name and default was compared with the page text. Removed the unfinished self-correction text, the invented Verify step and the unsupported placeholder and heading gotchas.

Method: documentation only; no commands were run.
