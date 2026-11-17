---
id: computing-software.cryptography-implementation.protocol-implementation.jwks-fetching-caching-and-kid-lookup
name: jwks-fetching-caching-and-kid-lookup
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, jwt, jose, jwks, kid, key-rotation, oidc-discovery, cache-control, rfc7517]
level: advanced
status: docs-checked
description: "Verify JWTs against a JWKS endpoint correctly: pinned issuer and JWKS URL, caching with refresh-on-unknown-kid and rate limits, kty/alg/use checks per key, and rotation timing."
sources: ["https://datatracker.ietf.org/doc/html/rfc7517", "https://openid.net/specs/openid-connect-discovery-1_0.html", "https://datatracker.ietf.org/doc/html/rfc8725", "https://github.com/panva/jose/blob/main/docs/jwks/remote/functions/createRemoteJWKSet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWKS fetching, caching and kid lookup

OIDC providers and token issuers publish signing keys as a JWK Set
(RFC 7517) at a `jwks_uri`. Verifiers must fetch, cache and select keys
without letting tokens choose where keys come from.

## Configuration, not token headers

- Pin the issuer (`iss`) and its JWKS URL in configuration (or derive the URL
  once from `https://issuer/.well-known/openid-configuration` at startup).
- Do not blindly follow `jku` or `x5u` headers (RFC 8725 warns of SSRF);
  ignore them and any embedded `jwk` header - key locations are configuration.
- One JWKS per trusted issuer; a token's `iss` selects the JWKS, and the
  signature check proves it.

## Key selection

1. Read `kid` from the token header; find the JWK with that `kid`.
2. Check the JWK is suitable: `kty` matches the expected algorithm family,
   `use` is `sig` (if present), `alg` (if present) equals the token's `alg`,
   and the token `alg` is in your allowlist (`RS256`, `ES256`, `EdDSA`...).
3. If no `kid` match: refresh the JWKS (see below) and retry once; then reject.

## Caching

- Cache the JWKS respecting `Cache-Control` max-age, with your own floor and
  ceiling.
- **Refresh on unknown kid**, rate-limited with a cooldown, so a flood of tokens with random `kid`s cannot make you hammer the
  IdP or DoS yourself.
- On fetch failure keep serving the last good JWKS (stale-if-error) for a
  bounded time.

```js
import { createRemoteJWKSet, jwtVerify } from 'jose';
// jose refetches on an unmatched key only after `cooldownDuration` has elapsed
const JWKS = createRemoteJWKSet(new URL('https://idp.example.com/.well-known/jwks.json'));
const { payload } = await jwtVerify(token, JWKS, {
  issuer: 'https://idp.example.com', audience: 'api://orders', algorithms: ['RS256', 'ES256'] });
```

## Rotation (issuer side)

Publish the new key in the JWKS at least one max cache period before signing
with it; keep the old key published until all tokens signed with it have
expired. See signing key rollover in the key rotation skill.

## Verify

- [ ] Tokens with `jku`/`x5u`/`jwk` headers pointing elsewhere are rejected or ignored.
- [ ] Unknown-kid storms trigger at most one refresh per cooldown.
- [ ] Algorithm allowlist and per-key `kty`/`alg` checks enforced.

## Checked

2026-10-31. Confirmed in RFC 8725 (`kid` lookup, `jku`/`x5u` SSRF warning), the
OpenID Connect Discovery spec (`jwks_uri`, `/.well-known/openid-configuration`)
and the jose `createRemoteJWKSet` page (cooldown-gated refetch on unmatched key;
selection by `alg`, `kid`, `use`). Removed: the numeric cache floors, ceilings
and cooldowns, the `cacheMaxAge` option, and the PyJWKClient and Nimbus lines.

Method: documentation only; no commands were run.
