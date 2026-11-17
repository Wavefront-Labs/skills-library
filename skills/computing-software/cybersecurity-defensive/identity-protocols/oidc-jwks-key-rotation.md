---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-jwks-key-rotation
name: oidc-jwks-key-rotation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-jwks-key-rotation, oidc-discovery, jwks, jwks_uri, kid, key-rotation, cache, identity-protocols]
level: advanced
status: docs-checked
description: "Fetch and cache the OP jwks_uri keys, select by kid, refresh on unknown kid with rate limiting, and rotate keys without outage."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://openid.net/specs/openid-connect-discovery-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWKS retrieval and signing key rotation

Goal: verify tokens across key changes.

Method (RP): the `jwks_uri` comes from the discovery document and holds the signing keys (and possibly encryption keys, then `use` is required on every key). Select the key by the `kid` in the JOSE header (required when the set has several keys). When you see an unfamiliar `kid`, go back to `jwks_uri` and retrieve the keys again. The JWKS response should carry `Cache-Control` with `max-age`, so you can cache it.

Method (OP): publish keys at `jwks_uri`; roll over by adding new keys to the set. The signer may begin using the new key at its discretion and signals it with `kid`. Keep recently decommissioned signing keys in the set for a reasonable period.

Gotchas:
- The JWK set must not contain private or symmetric key values.
- ID Tokens should not use `jku`, `jwk`, `x5u` or `x5c` header parameters: key references are communicated in advance via Discovery and Registration.
- Using one key for both signing and encryption is not recommended.

Verify: rotate in staging and watch for validation errors on live tokens.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 2 and 10.1.1 and Discovery section 3. Removed: the 5-minute refetch interval, rate-limit and fingerprinting advice, "publish the key before using it", the TLS-verification remark and the "keys with no kid" advice, none of which are stated.
Method: documentation only; no commands were run.
