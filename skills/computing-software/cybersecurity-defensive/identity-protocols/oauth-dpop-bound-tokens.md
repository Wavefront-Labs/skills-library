---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-dpop-bound-tokens
name: oauth-dpop-bound-tokens
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-dpop-bound-tokens, oauth-dpop, dpop-bound, cnf, jkt, refresh-token-binding, token-type-dpop, identity-protocols]
level: advanced
status: docs-checked
description: "Bind access tokens to the DPoP key via cnf.jkt, validate binding at the resource server, and bind refresh tokens for public clients."
sources:
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DPoP-bound access and refresh tokens

Goal: make a stolen token unusable without the key.

Method: the AS verifies the proof at the token endpoint and returns `token_type: DPoP`; JWT access tokens carry `cnf: {"jkt": "<base64url SHA-256 JWK thumbprint>"}`; opaque tokens return the same via introspection. The RS computes the thumbprint of the proof's `jwk` and compares it to `cnf.jkt`. Refresh tokens issued to public clients are bound to the same key and require a proof at refresh. Authorization codes can be bound with `dpop_jkt` on the authorization request.

Gotchas:
- A `Bearer`-scheme request with a DPoP-bound token must be refused.
- Metadata: `dpop_signing_alg_values_supported`, protected resource metadata `dpop_bound_access_tokens_required`.

Verify: replay the access token with a different key and expect invalid_token.

## Checked

2026-11-02. Confirmed against RFC 9449 sections 5, 6, 7.2 and 10 (`token_type` DPoP, `cnf` `jkt`, introspection, binding of public-client refresh tokens, rejecting a DPoP-bound token sent as Bearer, `dpop_jkt`, `dpop_signing_alg_values_supported`) and RFC 9728 (`dpop_bound_access_tokens_required`). Removed: the key-loss UX remark.
Method: documentation only; no commands were run.
