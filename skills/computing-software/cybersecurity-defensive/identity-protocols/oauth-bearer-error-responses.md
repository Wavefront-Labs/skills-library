---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-bearer-error-responses
name: oauth-bearer-error-responses
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-bearer-error-responses, oauth-bearer-tokens, www-authenticate, invalid_token, insufficient_scope, 401, 403, identity-protocols]
level: practitioner
status: docs-checked
description: "Return RFC 6750 WWW-Authenticate challenges with error invalid_request, invalid_token and insufficient_scope plus scope and realm attributes."
sources:
  - https://www.rfc-editor.org/rfc/rfc6750
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource server error responses

Goal: give clients a machine-readable reason.

- No credentials: `401` with `WWW-Authenticate: Bearer realm="api"` and no error code.
- Expired, revoked or malformed token: `401` with `Bearer error="invalid_token", error_description="..."`.
- Malformed request: `400` `invalid_request`.
- Valid token but not enough privilege: `403` `Bearer error="insufficient_scope", scope="orders:write"`.
- Metadata pointer (RFC 9728): `resource_metadata="https://api.example/.well-known/oauth-protected-resource"`.

Gotchas:
- Use 403 with `insufficient_scope` when the token is valid but lacks privilege (RFC 6750 section 3.1); the `scope` attribute is optional.
- DPoP uses scheme `DPoP` in the challenge.

Verify: call with an expired token and check the exact header.

## Checked

2026-11-02. Confirmed against RFC 6750 section 3 (`realm`, optional `scope`, no error code when credentials are absent, `invalid_request` 400, `invalid_token` 401, `insufficient_scope` 403), RFC 9728 (`resource_metadata` in `WWW-Authenticate: Bearer`) and RFC 9449 section 7.1 (`WWW-Authenticate: DPoP`). Removed: the advice on hiding revoked versus expired tokens and on refresh loops.
Method: documentation only; no commands were run.
