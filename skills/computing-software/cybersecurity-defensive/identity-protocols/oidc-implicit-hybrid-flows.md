---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-implicit-hybrid-flows
name: oidc-implicit-hybrid-flows
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-implicit-hybrid-flows, oidc-core-flows, implicit, hybrid, c_hash, at_hash, response_type, id_token-token, identity-protocols]
level: advanced
status: docs-checked
description: "Understand OIDC implicit and hybrid response_type values, c_hash and at_hash validation, and why new apps should use code with PKCE."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://openid.net/specs/oauth-v2-multiple-response-types-1_0.html
  - https://www.rfc-editor.org/rfc/rfc9700.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit and Hybrid flows, c_hash and at_hash

Goal: read legacy implicit/hybrid integrations and migrate them.

Response types: `id_token`, `id_token token` (implicit); `code id_token`, `code token`, `code id_token token` (hybrid). For all of these the default response mode is the fragment and the query encoding must not be used.
- `at_hash`: base64url of the left-most half of the hash of the access token, using the hash algorithm of the ID Token `alg` (SHA-256 for RS256). Required in the ID Token for `id_token token` and `code id_token token`.
- `c_hash`: same construction over the authorization code (for example SHA-512 for HS512). Required when the ID Token is issued with a code (`code id_token`, `code id_token token`).
- `nonce` is required for the implicit flow and for the hybrid types `code id_token` and `code id_token token`; optional for `code token`.

Gotchas:
- Core says the implicit flow is not designed to mitigate token substitution; at_hash and c_hash let the client detect substituted tokens.
- RFC 9700 says clients should not use the implicit grant (response type `token`) or other response types issuing access tokens in the authorization response unless the issues are mitigated.
- Modern apps: use the code flow with PKCE.

Verify: compute the hash by script and compare to the claim.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 3.2.2.10, 3.3.2.11, 16.11, the Multiple Response Type Encoding Practices spec and RFC 9700 section 2.1.2. Removed: "tokens in browser history and referrer", and the `response_mode=query` suggestion for SPAs.
Method: documentation only; no commands were run.
