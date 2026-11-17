---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-request-object
name: oidc-request-object
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-request-object, oidc-client-authentication, request-object, request_uri, signed-request, jwt, oidc-core, identity-protocols]
level: advanced
status: docs-checked
description: "Pass authorization parameters as a signed request object (request or request_uri) in OIDC Core section 6, with the claims, algorithms and validation rules."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://www.rfc-editor.org/rfc/rfc9101.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request objects and request_uri

Goal: protect request integrity and hide parameters.

Method: build a JWT whose claims are the authorization parameters (`response_type`, `client_id`, `redirect_uri`, `scope`, `state`, `nonce`, `claims` and so on), sign it (and optionally encrypt; sign then encrypt), and send `request=<JWT>` or `request_uri=<URL>` (not both). If signed, the object should contain `iss` (the client ID unless signed by another party) and `aud` (the OP's issuer URL). `response_type` and `client_id` must also be sent as plain OAuth parameters and match the object; `scope` must always be sent plainly with `openid`. Register `request_object_signing_alg` and optionally `request_uris`.

Gotchas:
- `request_uri` must use https unless the object is signed in a way the OP can verify; the OP must be able to reach it. Keep it unguessable and remove it when no longer needed, because it may contain requested claims.
- Values inside the object supersede plain query parameters.
- The OP must return an error if decryption or signature validation fails; the `alg` header must match the registered `request_object_signing_alg`.
- Use a unique URI per distinct request, or include a base64url SHA-256 hash of the content as the fragment, so caches are not stale.
- OPs advertise `request_parameter_supported`, `request_uri_parameter_supported` and `require_request_uri_registration`.
- The Core request object is compatible with JAR (RFC 9101).

Verify: alter one claim after signing and confirm the OP refuses the request.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 section 6 (6.1, 6.2, 6.3) and Discovery section 3. Removed: SSRF/replay surface claims, "OpenID parameter claims are the basis of JAR" wording and the pointer to PAR.
Method: documentation only; no commands were run.
