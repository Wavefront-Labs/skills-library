---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-pushed-authorization-requests
name: oauth-pushed-authorization-requests
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-pushed-authorization-requests, oauth-par-jar-rar, par, rfc9126, request_uri, pushed_authorization_request_endpoint, back-channel, identity-protocols]
level: advanced
status: docs-checked
description: "Send authorization parameters to the pushed_authorization_request_endpoint over an authenticated back channel and redirect with a request_uri."
sources:
  - https://www.rfc-editor.org/rfc/rfc9126
  - https://www.rfc-editor.org/rfc/rfc9101
  - https://www.rfc-editor.org/rfc/rfc9396
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pushed Authorization Requests (PAR)

Goal: keep parameters out of the browser and authenticate them.

Method:
1. Client POSTs the usual authorization parameters (with PKCE challenge, redirect_uri, scope, state) to the PAR endpoint, authenticating as the client where it has credentials.
2. AS validates the request and returns `201 Created` with JSON `request_uri` and `expires_in` (RFC 9126 shows `urn:ietf:params:oauth:request_uri:<reference>` and an `expires_in` of 60 in one example).
3. Client redirects the browser to the authorization endpoint with only `client_id` and `request_uri`.
The `request_uri` is a single-use reference (the AS SHOULD treat it as one-time use) and an expired one MUST be rejected. Metadata: `pushed_authorization_request_endpoint`, `require_pushed_authorization_requests`.

Gotchas:
- PAR lets the AS authenticate the client and refuse illegitimate requests before any user interaction.
- The request is sent directly to the AS, so URL size restrictions no longer apply (the AS may still answer 413 for oversized requests).
- New redirect URIs per request may be accepted only from authenticated clients (RFC 9126 security considerations).

Verify: reuse a request_uri and expect failure.

## Checked

2026-11-02. Confirmed against RFC 9126 (request, 201 response, `request_uri` single use and expiry, 413, client authentication benefit, redirect URI rule, metadata names). Removed: the rule on extra parameters next to `request_uri`, the FAPI 2.0 statement and the fixed `abc` value.
Method: documentation only; no commands were run.
