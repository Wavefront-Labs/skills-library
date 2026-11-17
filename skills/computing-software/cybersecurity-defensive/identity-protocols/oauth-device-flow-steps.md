---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-device-flow-steps
name: oauth-device-flow-steps
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-device-flow-steps, oauth-device-grant, device-flow, rfc8628, device_code, user_code, verification_uri, device_authorization_endpoint, identity-protocols]
level: practitioner
status: docs-checked
description: "Run the device flow: POST to device_authorization_endpoint, show user_code and verification_uri, poll the token endpoint with the device_code grant."
sources:
  - https://www.rfc-editor.org/rfc/rfc8628
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device authorization flow steps

Goal: sign in on input-constrained devices and CLIs.

Method:
1. Device POSTs `client_id` and `scope` to `device_authorization_endpoint`.
2. Response: `device_code`, `user_code`, `verification_uri` (and `verification_uri_complete`), `expires_in`, `interval` (default 5).
3. Device displays the code and URL (or QR from `verification_uri_complete`).
4. User opens the URL on another device, authenticates, enters the code and approves.
5. Device polls the token endpoint with `grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=...&client_id=...`.

Gotchas:
- `user_code` should be short, case-insensitive, from an unambiguous alphabet (BCDFGHJKLMNPQRSTVWXZ) with enough entropy and rate limiting on entry.
- Do not poll after `expired_token` or `access_denied`.

Verify: let the code expire and check the final error.

## Checked

2026-11-02. Confirmed against RFC 8628 sections 3.1 to 3.5 and 6.1 (request and response parameters, 5 second default interval, polling grant type, stop on `expired_token` and `access_denied`, user code alphabet, case-insensitivity, entropy and rate limiting). Removed: the statement on public client ids.
Method: documentation only; no commands were run.
