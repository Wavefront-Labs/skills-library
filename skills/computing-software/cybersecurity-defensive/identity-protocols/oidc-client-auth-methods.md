---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-client-auth-methods
name: oidc-client-auth-methods
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-client-auth-methods, oidc-client-authentication, client_secret_basic, client_secret_post, private_key_jwt, client_secret_jwt, token_endpoint_auth_method, identity-protocols]
level: practitioner
status: docs-checked
description: "Choose among client_secret_basic, client_secret_post, client_secret_jwt, private_key_jwt, tls_client_auth and none with their trade-offs."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://www.rfc-editor.org/rfc/rfc8705.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token endpoint client authentication methods

Goal: authenticate confidential clients with a registered method.

- `client_secret_basic`: HTTP Basic (RFC 6749 section 2.3.1); the default if none is registered.
- `client_secret_post`: credentials in the request body.
- `client_secret_jwt`: a JWT signed with an HMAC SHA algorithm using the UTF-8 octets of the `client_secret` as key.
- `private_key_jwt`: the client signs a JWT with a registered key. Required claims: `iss` and `sub` both equal to the `client_id`, `aud` (should be the token endpoint URL), `jti` (a token may be used only once unless negotiated), `exp`; `iat` is optional. Sent as `client_assertion` with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`.
- `tls_client_auth` / `self_signed_tls_client_auth` are defined by RFC 8705.
- `none` for public clients with no secret or other mechanism.

Gotchas:
- The OP lists the methods it supports in `token_endpoint_auth_methods_supported`; Discovery names `client_secret_post`, `client_secret_basic`, `client_secret_jwt` and `private_key_jwt`.
- The `alg` `none` must not be used for the assertion signature (`token_endpoint_auth_signing_alg_values_supported`).

Verify: check discovery for `token_endpoint_auth_methods_supported` and test each method you register.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 section 9, Discovery section 3 and RFC 8705 (method names). Removed: "weaker, rarely worth it", the FAPI requirement, the `jti` "keep exp under a few minutes" advice, URL-encoding of Basic secrets, `aud` "or issuer", the `invalid_client` check and the jwks_uri rotation remark.
Method: documentation only; no commands were run.
