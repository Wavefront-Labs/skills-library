---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-as-metadata
name: oauth-as-metadata
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-as-metadata, oauth-metadata-issuer, rfc8414, oauth-authorization-server, metadata, well-known, issuer, identity-protocols]
level: practitioner
status: docs-checked
description: "Publish and consume /.well-known/oauth-authorization-server metadata: issuer, endpoints, grant_types_supported, PKCE methods and the path-insertion rule."
sources:
  - https://www.rfc-editor.org/rfc/rfc8414
  - https://www.rfc-editor.org/rfc/rfc9207
  - https://www.rfc-editor.org/rfc/rfc9728
  - https://www.rfc-editor.org/rfc/rfc9126
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization server metadata (RFC 8414)

Goal: discover endpoints for non-OIDC OAuth servers.

Method: GET `https://host/.well-known/oauth-authorization-server` followed by the issuer's path component, if it has one (the well-known segment is inserted between host and path). Fields: `issuer` (required), `authorization_endpoint`, `token_endpoint`, `jwks_uri`, `registration_endpoint`, `scopes_supported`, `response_types_supported`, `grant_types_supported`, `token_endpoint_auth_methods_supported`, `revocation_endpoint`, `introspection_endpoint`, `code_challenge_methods_supported`, `dpop_signing_alg_values_supported`, `pushed_authorization_request_endpoint`, `require_pushed_authorization_requests`, `authorization_response_iss_parameter_supported`. Signed metadata uses `signed_metadata`.

Gotchas:
- The `issuer` in the document must equal the URL used to derive it; clients must check this to avoid impersonation.
- OIDC providers use `/.well-known/openid-configuration` (suffix form); try both if unsure.
- Metadata is served over TLS: the issuer is an `https` URL and implementations must support TLS (RFC 8414 section 6.1).

Verify: curl and compare `issuer` to the request URL.

## Checked

2026-11-02. Confirmed against RFC 8414 (well-known insertion rule, metadata field names, `issuer` identical to the derived URL, `https` issuer, TLS requirement, `openid-configuration` compatibility, `signed_metadata`), RFC 9126 (`pushed_authorization_request_endpoint`, `require_pushed_authorization_requests`), RFC 9449 (`dpop_signing_alg_values_supported`) and RFC 9207 (`authorization_response_iss_parameter_supported`). Reworded: the literal `{issuer-path}` placeholder and the http statement.
Method: documentation only; no commands were run.
