---
id: computing-software.cybersecurity-defensive.zitadel.jwks-key-rotation-and-caching
name: jwks-key-rotation-and-caching
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, jwks, signing-keys, key-rotation, caching, jwt-validation]
level: advanced
status: docs-checked
description: "Validate ZITADEL JWTs locally with the JWKS endpoint, cache the key set sensibly and plan for keys that rotate without notice."
sources:
  - https://zitadel.com/docs/apis/openidoauth/endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The JWKS endpoint, `${CUSTOM_DOMAIN}/oauth/v2/keys`, returns the public keys for validating JWTs issued by ZITADEL locally. The alternative is the introspection endpoint.

Rotation: keys are rotated automatically on a regular basis or on demand, so they change at irregular intervals and without prior notice. ZITADEL sets a proper `kid` on each key, so match tokens to keys by `kid`.

Caching: caching the response improves performance. Without a cache you call the endpoint on every request, and a large number of requests from one backend can get you rate limited. Because keys can rotate unannounced, refresh the cache regularly. The documentation also suggests combining caching with a risk-based refresh on demand when a critical operation runs.

A sound implementation:

1. Cache the key set keyed by `kid`.
2. On an unknown `kid`, refetch once, then fail the request if still unknown.
3. Refresh on a timer as well.
4. For high-risk actions, use introspection, which also checks revocation.

Local validation cannot see revocation or logout, so choose between speed and freshness per endpoint.

## Checked
2026-11-08. Confirmed against the ZITADEL OIDC endpoints page: JWKS endpoint path, automatic or on-demand rotation without notice, kid on each key, caching and risk-based refresh advice, rate-limit warning, and the introspection endpoint checking revocation. The numbered implementation steps are advice built on those statements.
Method: documentation only; no commands were run.
