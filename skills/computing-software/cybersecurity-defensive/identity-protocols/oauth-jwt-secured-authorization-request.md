---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-jwt-secured-authorization-request
name: oauth-jwt-secured-authorization-request
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-jwt-secured-authorization-request, oauth-par-jar-rar, jar, rfc9101, request-object, signed-request, require_signed_request_object, identity-protocols]
level: advanced
status: docs-checked
description: "Wrap authorization parameters in a signed (and optionally encrypted) request object per RFC 9101, with required claims, aud and algorithm rules."
sources:
  - https://www.rfc-editor.org/rfc/rfc9101
  - https://www.rfc-editor.org/rfc/rfc9126
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT-Secured Authorization Request (JAR)

Goal: protect integrity and authenticity of the authorization request.

Method (RFC 9101): the Request Object is a JWT whose claims are the authorization request parameters; it MUST contain all parameters used to process the request (`response_type`, `client_id`, `redirect_uri`, `scope`, `state`, `code_challenge` and so on) except `request` and `request_uri`. If signed (JWS), it SHOULD contain `iss` and `aud`, where `aud` should be the authorization server's issuer. Send it by value as the `request` parameter or by reference as `request_uri`; the client may also pass it to a PAR endpoint (RFC 9126). Metadata: `require_signed_request_object` (client and server; when true the server rejects a Request Object whose `alg` is `none`), `request_object_signing_alg_values_supported` (server metadata); clients register `request_object_signing_alg`.

Gotchas:
- The AS MUST use only the parameters inside the Request Object, even if the same parameter appears in the query, and the `client_id` request parameter and the object's `client_id` claim MUST be identical.
- A `request_uri` must be an https URI (or a URN when the AS issued it) and the AS must be able to reach it; a Request Object URI can be replayed, so its lifetime MUST be short and preferably one-time use, with enough entropy (the RFC gives a validity of less than a minute and 128 bits or more of cryptographic randomness as general guidance).
- When signing and encrypting, the JWT MUST be signed first, then encrypted (nested JWT).
- `exp`, `nbf` and `jti` are registered by RFC 9101 as JWT claims usable in authorization requests; it gives no lifetime values for them.

Verify: change `redirect_uri` outside the Request Object and confirm it is ignored.

## Checked

Date: 2026-11-02. Confirmed in RFC 9101 (Request Object, request and request_uri, server processing, metadata and security considerations) and RFC 9126 (PAR carries Request Objects). Removed as not stated there: "prefer PAR" and SSRF wording, "short exp/nbf" advice beyond the registered names, the `login_hint` PII example, and RFC 9396 as a source (see the RAR skill).

Method: documentation only; no commands were run.
