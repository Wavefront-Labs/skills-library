---
id: computing-software.cybersecurity-defensive.identity-protocols.ciba-token-delivery-modes
name: ciba-token-delivery-modes
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [ciba-token-delivery-modes, oidc-ciba, ciba, poll, ping, push, client_notification_endpoint, urn:openid:params:grant-type:ciba, identity-protocols]
level: advanced
status: docs-checked
description: "Choose the CIBA token delivery mode: poll the token endpoint with interval, ping notification, or push the tokens, and register the notification endpoint correctly."
sources:
  - https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIBA poll, ping and push delivery

Goal: get tokens after the user approves.

Register `backchannel_token_delivery_mode` as `poll`, `ping` or `push` (a client can register only one). `backchannel_client_notification_endpoint` is required for ping and push and MUST be an HTTPS URL; communication with it MUST use TLS.

- Poll: POST to the token endpoint with `grant_type=urn:openid:params:grant-type:ciba` and `auth_req_id`, no more often than `interval` (default 5 seconds if absent). Long polling is allowed (30-second timeout recommended). Errors: `authorization_pending`, `slow_down` (interval MUST increase by at least 5 seconds for this and all later requests), `expired_token`, `access_denied`.
- Ping: after success or failure the OP POSTs JSON containing only `auth_req_id` to the notification endpoint with `Authorization: Bearer <client_notification_token>`. The client verifies the token (401 if invalid), answers 204 (200 accepted), never a 3xx, then calls the token endpoint.
- Push: the OP POSTs a JSON payload with ID Token, access token, optional refresh token and `auth_req_id`, authenticated with the same bearer. The ID Token MUST carry `at_hash` and the `urn:openid:params:jwt:claim:auth_req_id` claim (`rt_hash` for refresh tokens). The client validates the ID Token, checks `auth_req_id` matches and validates the access token with `at_hash`. Errors arrive as a Push Error Payload (`error`, `auth_req_id`, optional `error_description`; codes `access_denied`, `expired_token`, `transaction_failed`). A push client calling the token endpoint with the CIBA grant gets `unauthorized_client`.

The client sends `client_notification_token` (at most 1024 characters, at least 128 bits of entropy, 160 recommended) in the authentication request for ping or push.

Gotchas (spec section 14):
- Apply security controls to the notification endpoint and its registration; the OP SHOULD ensure the endpoint is in the client's administrative authority.
- Hashes and `auth_req_id` in the ID Token let the client detect tampering; sender-constrained access tokens are recommended.

Verify: approve a request and compare the three modes against the client metadata registered.

## Checked
Method: 2026-11-08 read the CIBA Core spec via a targeted fetch covering sections 4, 7, 10-14 (not the whole page). Removed as unsupported: "push not allowed with FAPI profiles" and the claim that proxies may log push callbacks.
