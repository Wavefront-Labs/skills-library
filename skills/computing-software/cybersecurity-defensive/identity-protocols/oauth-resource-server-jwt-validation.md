---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-resource-server-jwt-validation
name: oauth-resource-server-jwt-validation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-resource-server-jwt-validation, oauth-jwt-access-tokens, resource-server, validation, aud, issuer, jwks, scope-check, identity-protocols]
level: practitioner
status: docs-checked
description: "Validate incoming JWT access tokens at the API: issuer allow-list, signature via JWKS, typ, aud equals this API, exp, scope checks and tenant mapping."
sources:
  - https://www.rfc-editor.org/rfc/rfc9068
  - https://www.rfc-editor.org/rfc/rfc8707
  - https://www.rfc-editor.org/rfc/rfc8725
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource server validation of JWT access tokens

Goal: authorise requests correctly with minimal calls.

Method (RFC 9068 Section 4; the RS MUST validate in this manner):
- The `typ` header MUST be `at+jwt` or `application/at+jwt`; reject any other value.
- If the token is encrypted, decrypt it with the keys the RS specified at registration.
- The `iss` claim MUST exactly match the issuer identifier of the AS (typically obtained during discovery); AS metadata (RFC 8414) advertises the signing keys through `jwks_uri` and the expected `iss` through `issuer`.
- The `aud` claim MUST contain a resource indicator the RS expects for itself; otherwise reject (see also RFC 8707 resource indicators).
- Validate the signature per RFC 7515 with the algorithm in `alg`, reject `alg` of `none`, and use only keys provided by the AS. An AS and RS conforming to RFC 9068 MUST include RS256 among their supported signature algorithms; asymmetric algorithms are RECOMMENDED.
- The current time MUST be before `exp`, with at most a small leeway (usually no more than a few minutes) for clock skew.
- On any failure answer with the error code `invalid_token` (RFC 6750 Section 3.1).
- If the token has authorization claims (RFC 9068 Section 2.2.3), the RS SHOULD use them with other context to decide whether to authorise the call.

Gotchas:
- Check `aud`; RFC 9068 requires a distinct `aud` identifier per resource to prevent cross-JWT confusion, so tokens for other APIs from the same AS must be rejected here.
- RFC 8725: do not blindly follow `jku`/`x5u`; match against an allow-list.
- The AS may sign access tokens and ID tokens with any key advertised in its metadata, and the RS cannot tell which; the typed `at+jwt` header is what separates access tokens from ID tokens.

Verify: unit-test with a token for another audience and one signed by another issuer.

## Checked

Date: 2026-11-02. Confirmed in RFC 9068 Sections 2, 4 and 5, RFC 8707 (resource indicators) and RFC 8725 (jku/x5u). Removed as not stated there: the fixed algorithm list `RS256, PS256, ES256`, `nbf` and `iat` checks and the `iat` skew, JWKS caching with rate-limited refresh, "scopes grant what the client may do" advice, tenant and `sub` rules.

Method: documentation only; no commands were run.
