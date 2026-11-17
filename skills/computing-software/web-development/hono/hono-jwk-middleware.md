---
id: computing-software.web-development.hono.hono-jwk-middleware
name: hono-jwk-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, auth, jwk, jwks]
level: advanced
status: docs-checked
description: "Verify JWTs against public keys with the Hono jwk middleware: jwks_uri, keys, alg allowlist, allow_anon and verifyWithJwks outside middleware."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/jwk.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JWK auth middleware

Import: `import { jwk } from 'hono/jwk'` and `import { verifyWithJwks } from 'hono/jwt'`.

```ts
app.use('/auth/*', jwk({
  jwks_uri: `https://${backendServer}/.well-known/jwks.json`,
  alg: ['RS256'],
}))
app.get('/auth/page', (c) => c.json(c.get('jwtPayload')))
```

## What it validates
Parses the header, REQUIRES a `kid` and matches a key by it, rejects symmetric algs (`HS256/384/512`), requires header `alg` to be in your `alg` allowlist (and to equal the JWK's own `alg` if present), verifies the signature, and by default checks `nbf`, `exp`, `iat`. Optional `verification: { iss, aud }`. Extra authorization rules go in your own middleware after `jwk()`.

## Options
- `alg` (required): `RS256|RS384|RS512|PS256|PS384|PS512|ES256|ES384|ES512|EdDSA`.
- `keys`: `HonoJsonWebKey[]` or `(c) => Promise<HonoJsonWebKey[]>`.
- `jwks_uri`: string or `(c) => Promise<string>`; fetched keys are added to `keys`.
- `allow_anon: true`: let requests without a valid token pass; check `c.get('jwtPayload')` (e.g. `payload ?? { message: 'hello anon' }`).
- `cookie`, `headerName` (default `Authorization`), `realm`, `verification`.

## Fetch options for the JWKS request
Second argument is a `RequestInit` used only for fetching the JWKS:

```ts
jwk({ jwks_uri: `https://${backendServer}/.well-known/jwks.json`, alg: ['RS256'] },
    { headers: { Authorization: 'Bearer TOKEN' } })
```

## Outside middleware
```ts
const id_payload = await verifyWithJwks(
  id_token,
  { jwks_uri: 'https://your-auth-server/.well-known/jwks.json', allowedAlgorithms: ['RS256'] },
  { cf: { cacheEverything: true, cacheTtl: 3600 } }
)
```

## Gotcha
Tokens without a `kid`, or signed with HS* algorithms, are rejected. The client Authorization header needs a scheme such as `Bearer`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/jwk.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
