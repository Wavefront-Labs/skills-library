---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-authorization-request
name: oauth-authorization-request
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-authorization-request, oauth-core-framework, authorization-request, response_type, redirect_uri, scope, state, error-response, identity-protocols]
level: practitioner
status: docs-checked
description: "Compose a valid authorization request: response_type, client_id, redirect_uri, scope, state, code_challenge and the error response format."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization request parameters

Goal: send and interpret authorization requests.

Parameters: `response_type=code` (required), `client_id` (required), `redirect_uri` (required if several, a partial URI or none are registered; the AS compares it to the registered value with exact string matching), `scope` (space-delimited), `state` (CSRF token, returned unchanged), `code_challenge` and `code_challenge_method=S256`, optional `resource` (RFC 8707).

Error: redirect with `error`, `error_description`, `state`. Codes: `invalid_request`, `unauthorized_client`, `access_denied`, `unsupported_response_type`, `invalid_scope`, `server_error`, `temporarily_unavailable`. If the client_id or redirect_uri is invalid, do not redirect: show an error to the user.

Gotchas:
- Parameters must not repeat.
- The authorization endpoint must support GET and may support POST.
- `state` mismatch means abort; do not exchange the code.

Verify: send an invalid scope and check the redirect carries error=invalid_scope and state.

## Checked

2026-11-02. Confirmed against RFC 6749 sections 3.1, 3.1.2.3, 4.1.1 and 4.1.2.1 (parameters, error codes, no redirect on invalid client_id or redirect_uri, repeated parameters, GET MUST and POST MAY), RFC 9700 (exact string matching) and RFC 7636 and RFC 8707 (`code_challenge`, `resource`). Corrected: the `redirect_uri` requirement and the GET/POST rule.
Method: documentation only; no commands were run.
