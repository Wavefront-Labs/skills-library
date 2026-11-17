---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-token-endpoint-errors
name: oauth-token-endpoint-errors
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-token-endpoint-errors, oauth-core-framework, token-endpoint, invalid_grant, invalid_client, access_token, token_type, expires_in, identity-protocols]
level: practitioner
status: docs-checked
description: "Use the token endpoint correctly: form-encoded requests, client authentication, response fields and the invalid_grant, invalid_client and invalid_request errors."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://www.rfc-editor.org/rfc/rfc7636
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token endpoint request and error responses

Goal: call and debug /token.

Request: POST `application/x-www-form-urlencoded`. Success (200) returns JSON `access_token`, `token_type`, `expires_in`, optional `refresh_token`, `scope` (required if different from requested). Responses carry `Cache-Control: no-store` and `Pragma: no-cache`.

Errors (400 JSON): `invalid_request`, `invalid_client` (401 with `WWW-Authenticate` if attempted via header), `invalid_grant` (invalid, expired or revoked grant, `redirect_uri` mismatch, or a grant issued to another client), `unauthorized_client`, `unsupported_grant_type`, `invalid_scope`.

Gotchas:
- `invalid_grant` covers an expired or reused code, a `redirect_uri` mismatch and (RFC 7636) a wrong PKCE `code_verifier`.
- With HTTP Basic client authentication, the client id and secret are first encoded with `application/x-www-form-urlencoded`, then base64-encoded (RFC 6749 section 2.3.1).

Verify: reuse a code and confirm invalid_grant.

## Checked

2026-11-02. Confirmed against RFC 6749 sections 2.3.1, 5.1 and 5.2 (request format, success fields, `scope` rule, `Cache-Control: no-store` and `Pragma: no-cache`, error codes, 400 and 401 handling) and RFC 7636 (`invalid_grant` on verifier mismatch). Removed: the 60 second code lifetime, the claim that most failures are `invalid_grant`, and the logging advice.
Method: documentation only; no commands were run.
