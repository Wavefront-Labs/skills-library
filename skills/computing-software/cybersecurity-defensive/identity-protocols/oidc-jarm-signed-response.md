---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-jarm-signed-response
name: oidc-jarm-signed-response
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-jarm-signed-response, oidc-response-modes, jarm, response-jwt, signed-authorization-response, mix-up, identity-protocols]
level: sme
status: docs-checked
description: "Request and validate JARM responses: signed or encrypted authorization responses, error handling and the relationship to iss mix-up defence."
sources:
  - https://openid.net/specs/oauth-v2-jarm.html
  - https://www.rfc-editor.org/rfc/rfc9207.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT Secured Authorization Response Mode (JARM)

Goal: integrity-protect the authorization response.

Method: register `authorization_signed_response_alg` (default RS256; `none` not allowed) and optionally `authorization_encrypted_response_alg` / `authorization_encrypted_response_enc` (default `A128CBC-HS256` if the alg is given), then request `response_mode=jwt` (or `query.jwt`, `fragment.jwt`, `form_post.jwt`). The callback carries `response=<JWT>`. The client may decrypt, then must check `iss` is the expected issuer, `aud` equals the `client_id` it used, and `exp` has not passed, and verify the signature; the JWT also carries the authorization response parameters (for example `code`, `state`), including error responses.

Gotchas:
- `iss` and `aud` let the client detect mix-up attacks. RFC 9207 provides an `iss` response parameter as an alternative.
- A maximum JWT lifetime of 10 minutes is recommended.
- Check the issuer is a well-known expected one before fetching keys for it (denial of service via a crafted issuer).
- `query.jwt` must not be used with response types containing `token` or `id_token` unless the JWT is encrypted.
- An encrypted response does not remove the need for PKCE.
- OPs advertise support in `response_modes_supported`.

Verify: tamper with the `response` parameter and confirm validation fails.

## Checked
2026-11-02. Confirmed against the JARM specification (sections 2, 3, 4, 5) and RFC 9207. Removed: "not widely supported outside FAPI", "JARM is more complex than RFC 9207".
Method: documentation only; no commands were run.
