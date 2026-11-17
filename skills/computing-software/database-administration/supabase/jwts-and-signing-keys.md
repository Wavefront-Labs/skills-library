---
id: computing-software.database-administration.supabase.jwts-and-signing-keys
name: jwts-and-signing-keys
category: computing-software
field: database-administration
product: supabase
tags: [jwt, jwks, signing-keys, getclaims, hs256]
level: advanced
status: docs-checked
description: "Supabase JWT structure, claims, JWKS endpoint caching and rotation waits, getClaims, and why not to verify HS256 tokens with the shared secret."
sources:
  - https://supabase.com/docs/guides/auth/jwts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: issue, send and verify Supabase JWTs correctly.

JWTs underpin RLS: each product verifies the token before applying Postgres policies and roles. Auth issues a short-lived access token per signed-in user; publishable and secret API keys are converted on the fly into short-lived JWTs; a Custom Access Token Hook can change claims.

Header: `typ` JWT, `alg` HS256, ES256 or RS256, optional `kid`. Claims: `iss` (append `/.well-known/jwks.json` for public keys), `exp` (past it, untrusted even if signed), `sub` (user ID), `role` (Postgres role for RLS), plus `email`, `phone` and similar.

Send tokens as `Authorization: Bearer <jwt>`. Clients accept custom or third-party JWTs through an `accessToken` option; setting a custom `Authorization` header is no longer recommended.

Verification:
- `/auth/v1/.well-known/jwks.json` returns public keys only, and none unless asymmetric signing keys are in use.
- The Supabase Edge caches JWKS for 10 minutes; wait at least 20 minutes after creating a standby key or revoking one. Do not cache JWKS longer than needed and provide a purge method for rotation.
- `supabase.auth.getClaims()` is only for tokens issued by Supabase Auth; for JWTs minted with an imported key, verification may fail, so use a JWT verification library (the page's example uses `jose` with `createRemoteJWKSet` and `jwtVerify`).
- For HS256, the page recommends always checking tokens with `GET /auth/v1/user`, sending an `apikey` header (publishable key) and `Authorization: Bearer <JWT>`; HTTP 200 OK means valid, otherwise not. Supabase strongly advises against verifying HS256 with the shared secret (impersonation, leaks via `NEXT_PUBLIC_`, `VITE_` or `PUBLIC_` prefixes, compliance, hard rotation).
- Auth runs only in the project's region, so that check can be slow; avoid it from servers or functions running on the edge and prefer a server in the project's region.

## Checked

2026-11-04: Read the JWT guide in full. Confirmed structure, claims, JWKS behaviour, the 10 minute cache and 20 minute wait, the `accessToken` option and the HS256 advice. Added the `/auth/v1/user` request headers and the imported-key caveat for `getClaims()`.
Method: documentation only; no commands were run.
