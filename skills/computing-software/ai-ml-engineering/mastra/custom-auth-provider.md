---
id: computing-software.ai-ml-engineering.mastra.custom-auth-provider
name: custom-auth-provider
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, auth, rbac, jwks, authenticatetoken, authorizeuser, custom-provider]
level: advanced
status: docs-checked
description: "Write a custom Mastra auth provider by extending MastraAuthProvider: authenticateToken, authorizeUser, public/protected paths, JWKS verification and role-based rules."
sources:
  - https://mastra.ai/docs/auth/custom-auth-provider
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: integrate an identity system Mastra has no built-in provider for.

## Skeleton
Extend `MastraAuthProvider<TUser>` from `@mastra/core/server`:
- constructor: `super({ name })`, read config from options or env (throw if required values are missing), then call `this.registerOptions(options)` so `authorizeUser` overrides and `public`/`protected` paths are honoured.
- `authenticateToken(token, request)`: return the user, or `null` on failure. The token is taken from `Authorization: Bearer <token>`; use `getRequestHeader()` / `getWebRequest()` (from `@mastra/core/server`) on `request` for other headers or cookies.
- `authorizeUser(user, request)`: `true` allows; `false` returns 403 Forbidden.

Register it: `new Mastra({ server: { auth: new MyAuthProvider({...}) } })`.

## Options (`MastraAuthProviderOptions`)
`name`, `authorizeUser`, `protected`, `public`. Paths can be exact strings, wildcards (`'/api/*'`), RegExp, or `[path, method(s)]` tuples such as `['/api/webhook', 'POST']`. `public` paths bypass auth unless the route sets `requiresAuth: true`.

## Helpers from `@mastra/auth`
`verifyHmac(token, secret)`, `verifyJwks(token, jwksUrl)`, `decodeToken(token)` (no verification), `getTokenIssuer(decoded)`.

JWKS provider pattern: `authenticateToken` calls `verifyJwks(token, this.jwksUri)`, optionally rejects when `payload.iss !== this.issuer`, returns the payload, and catches errors to return `null`; `authorizeUser` rejects expired `exp` and requires `sub`.

## Role-based rules
Override `authorizeUser` and branch on the web request: admins only for `/admin/` paths, `write` or `admin` role for POST/PUT/PATCH/DELETE, everything else allowed for authenticated users. Return `false` if `getWebRequest(request)` is missing.

## Practices
- Fail safe: return `null` immediately for a non-string or empty token; log errors but do not expose details to the client.
- Test with Vitest by mocking `fetch`: assert valid token returns the user, `{ ok: false }` returns `null`, constructor throws when required options are absent, and `public`/`protected` are stored.
- Built-in providers to copy from: `MastraJwtAuth`, Clerk, Auth0, Supabase, Firebase, WorkOS, Better Auth (separate `@mastra/auth-*` packages) and `SimpleAuth`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
