---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-dynamic-client-registration
name: oauth-dynamic-client-registration
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-dynamic-client-registration, oidc-client-registration, dcr, rfc7591, registration_endpoint, client_metadata, initial-access-token, identity-protocols]
level: advanced
status: docs-checked
description: "Register clients at a registration_endpoint (RFC 7591): metadata fields, initial access token, client_id and secret issuance and error responses."
sources:
  - https://openid.net/specs/openid-connect-registration-1_0.html
  - https://www.rfc-editor.org/rfc/rfc7591
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic client registration request and response

Goal: automate client onboarding.

Method: POST JSON to `registration_endpoint` (optionally with an initial access token). Example fields: `redirect_uris`, `response_types`, `grant_types`, `application_type` (web/native), `client_name`, `token_endpoint_auth_method`, `jwks` or `jwks_uri`, `scope`, `logo_uri`, `software_id`, `software_statement`, `id_token_signed_response_alg`. The 201 response returns `client_id`, optional `client_secret` with `client_secret_expires_at`, and `registration_access_token` and `registration_client_uri` for management.

Gotchas:
- A server may accept open registration (no initial access token) or require an initial access token; software statements carry signed metadata (RFC 7591 section 3).
- Registered redirect URIs are compared with exact string matching at authorization time (RFC 9700).
- Errors: `invalid_redirect_uri`, `invalid_client_metadata`, `invalid_software_statement`.

Verify: register with an invalid `redirect_uris` value and confirm an `invalid_redirect_uri` error.

## Checked

2026-11-02. Confirmed against RFC 7591 (registration request, `201 Created` response, `client_secret_expires_at`, `software_statement`, initial access token, open registration, error codes) and OpenID Connect Dynamic Client Registration 1.0 (`application_type`, `id_token_signed_response_alg`, `registration_access_token`, `registration_client_uri`). Removed: the claim that open registration must be closed and the `javascript:` and `data:` redirect rules.
Method: documentation only; no commands were run.
