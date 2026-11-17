---
id: computing-software.cybersecurity-defensive.identity-protocols.ciba-authentication-request
name: ciba-authentication-request
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [ciba-authentication-request, oidc-ciba, ciba, backchannel_authentication_endpoint, auth_req_id, binding_message, login_hint_token, identity-protocols]
level: advanced
status: docs-checked
description: "Start a decoupled login at backchannel_authentication_endpoint with scope, one hint, binding_message and user_code, and handle the auth_req_id response and errors."
sources:
  - https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIBA authentication request

Goal: authenticate a user on a separate device without a browser redirect.

Method: client-authenticated POST over TLS to `backchannel_authentication_endpoint` (section 7).
- `scope`: REQUIRED, must include `openid`.
- Exactly one hint ("one and only one"): `login_hint` (email, phone, username), `login_hint_token` (format deployment-specific; SHOULD be signed per section 14) or `id_token_hint`. More than one gives `invalid_request`.
- Optional: `binding_message`, `user_code`, `acr_values` (space-separated, in preference order), `requested_expiry` (positive integer the OP MAY use), and `client_notification_token` (required for ping or push; at most 1024 characters, at least 128 bits of entropy).
- `user_code` is only sent when the client's `backchannel_user_code_parameter` indicates support; the client MUST NOT store it, but ask the user each flow.
- Response (7.3): `auth_req_id` (opaque, at least 128 bits entropy, characters A-Z a-z 0-9 . - _), `expires_in` (seconds), `interval` (only for poll or ping; default 5).

Gotchas:
- Errors (section 13): HTTP 400 `invalid_request`, `invalid_scope`, `expired_login_hint_token`, `unknown_user_id`, `unauthorized_client`, `missing_user_code`, `invalid_user_code`, `invalid_binding_message`; 401 `invalid_client`; 403 `access_denied`.
- `binding_message` is shown on both devices so the user can link them; it SHOULD be relatively short with a limited set of plain-text characters, and should contain something like a random value or approval code. The spec gives no numeric length limit.

Verify: send a request with two hints and expect `invalid_request`.

## Checked
Method: 2026-11-08 read CIBA Core sections 7, 13 and 14 via a targeted fetch. Removed as unsupported: the "about 20 chars" limit and the advice to use `user_code` where hints are guessable (the spec text read does not state it).
