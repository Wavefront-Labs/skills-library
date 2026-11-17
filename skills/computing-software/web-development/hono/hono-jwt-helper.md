---
id: computing-software.web-development.hono.hono-jwt-helper
name: hono-jwt-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, jwt, auth, tokens]
level: practitioner
status: docs-checked
description: "Sign, verify and decode JWTs in Hono with sign, verify and decode from hono/jwt, claim checks, algorithms and error classes."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/jwt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JWT helper

Import: `import { decode, sign, verify } from 'hono/jwt'`.

## sign
`sign(payload, secret, alg?)` returns `Promise<string>`; default alg is HS256.

```ts
const payload = {
  sub: 'user123',
  role: 'admin',
  exp: Math.floor(Date.now() / 1000) + 60 * 5, // 5 minutes
}
const token = await sign(payload, 'mySecretKey')
```

## verify
`verify(token, secret, alg, issuer?, aud?)` returns the payload; `alg` is required.

```ts
const decodedPayload = await verify(tokenToVerify, secretKey, 'HS256')
```
`issuer` is `string | RegExp`; `aud` is `string | string[] | RegExp` (if set the token must carry a matching `aud`).

## decode
`decode(token)` returns `{ header, payload }` WITHOUT verifying the signature. The page says it is useful for debugging or extracting information; use `verify()` to trust a token.

## Payload validation
During verify: `exp` (not expired), `nbf` (not before), `iat` (not in the future), `iss` (trusted issuer), `aud` (when set). The payload must contain these fields as an object for the checks to apply.

## Error classes
`JwtAlgorithmNotImplemented`, `JwtTokenInvalid`, `JwtTokenNotBefore`, `JwtTokenExpired`, `JwtTokenIssuedAt`, `JwtTokenIssuer`, `JwtPayloadRequiresAud`, `JwtTokenAudience`, `JwtTokenSignatureMismatched`.

## Algorithms
HS256/384/512, RS256/384/512, PS256/384/512, ES256/384/512 (ES512 uses P-521), EdDSA (Ed25519).

## Gotcha
`decode()` extracts the header and payload WITHOUT performing signature verification, so use `verify()` when you need to trust a token. The docs example for `sign()` includes `exp: Math.floor(Date.now() / 1000) + 60 * 5` (token expires in 5 minutes).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/jwt.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); "debugging only" (reworded to the page).

Method: documentation only; no commands were run.
