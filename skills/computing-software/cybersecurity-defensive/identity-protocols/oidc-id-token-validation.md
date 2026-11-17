---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-id-token-validation
name: oidc-id-token-validation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-id-token-validation, oidc-id-token, id-token-validation, jwks, signature, nonce, alg, validation, identity-protocols]
level: advanced
status: docs-checked
description: "Validate an ID token in order: signature and alg, iss, aud and azp, exp and iat, nonce, auth_time and hash claims, with library-use guidance."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ID token validation steps

Goal: accept only tokens meant for this client from the right issuer.

Order (Core 3.1.3.7):
1. If encrypted, decrypt with the key and algorithm registered; if encryption was negotiated and the token is not encrypted, the RP should reject it.
2. `iss` must exactly match the issuer identifier (typically from discovery).
3. `aud` must contain the client's `client_id`; reject if it contains additional audiences the client does not trust. If `azp` is present, the client should verify it equals its `client_id`.
4. Token received directly from the token endpoint over TLS: TLS server validation may replace signature checking. Otherwise validate the JWS signature with the issuer's keys; `alg` should be RS256 or the value registered in `id_token_signed_response_alg`. For MAC algorithms (`HS256` and so on) the key is the UTF-8 octets of the `client_secret`.
5. Current time must be before `exp`; Core allows small leeway for clock skew, usually no more than a few minutes. `iat` can be used to reject tokens issued too far from the present (the range is client specific).
6. If a `nonce` was sent, the claim must be present and equal.
7. If `acr` was requested, check it is appropriate. If `auth_time` was requested (or `max_age` used), check it and re-authenticate if too old.
8. `at_hash` / `c_hash`, when present, can be checked against the access token / code.

Gotchas:
- `alg` `none` must not be used unless the response type returns no ID Token from the authorization endpoint (such as the code flow) and the client explicitly requested it at registration.
- Reject the token if the `aud` claim lacks your client ID, even if the signature is valid.

Verify: unit test with expired, wrong-aud and wrong-nonce tokens.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 2 and 3.1.3.7. Removed: "azp is present and equals client_id when aud has multiple values" (Core's rule is different), "HS256 with a public key confusion" and "validating anyway is safer".
Method: documentation only; no commands were run.
