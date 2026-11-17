---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-id-token-claims
name: oidc-id-token-claims
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-id-token-claims, oidc-id-token, id_token, iss, sub, aud, exp, iat, auth_time, acr, amr, azp, identity-protocols]
level: practitioner
status: docs-checked
description: "Know the required and optional ID token claims: iss, sub, aud, exp, iat, auth_time, nonce, acr, amr, azp, at_hash and c_hash with their meaning."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://www.rfc-editor.org/rfc/rfc8176.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ID token claims reference

Goal: know what an ID token asserts.

Required: `iss` (https URL, no query or fragment), `sub` (locally unique, never reassigned, at most 255 ASCII characters), `aud` (must contain the client's `client_id`; may be an array), `exp`, `iat`.
Conditional or optional: `auth_time` (required when `max_age` was requested or `auth_time` was requested as essential), `nonce` (must be included when sent in the request), `acr` (the value "0" means the authentication did not meet ISO/IEC 29115 level 1; use an absolute URI or an RFC 6711 registered name), `amr` (array of method identifiers such as `pwd`, `otp`, `hwk`, registered under RFC 8176), `azp` (client ID of the party the token was issued to), `at_hash`, `c_hash`.

Gotchas:
- ID Tokens must be signed with JWS and may then be encrypted (nested JWT); they should not use the `x5u`, `x5c`, `jku` or `jwk` header parameters.
- Core says the `azp` claim in practice appears only when extensions are used, so implementations not using such extensions should ignore it.
- `exp` is unrelated to the lifetime of the session between the RP and OP.
- Unknown claims in an ID Token must be ignored.

Verify: decode (base64url) the payload and check each claim against the above.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 section 2 and 3.1.3.6, and RFC 8176 (`pwd`, `otp`, `hwk`). Removed: "`azp` present if aud has multiple values" (Core says otherwise), "rely on `acr` rather than `amr`", "do not send the ID token to resource servers", and the `email` change/reassignment remark.
Method: documentation only; no commands were run.
