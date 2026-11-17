---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-client-management-rfc7592
name: oauth-client-management-rfc7592
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-client-management-rfc7592, oidc-client-registration, rfc7592, registration_client_uri, registration_access_token, client-update, client-delete, identity-protocols]
level: advanced
status: docs-checked
description: "Read, update and delete a dynamically registered client at registration_client_uri with the registration_access_token (RFC 7592), including secret rotation."
sources:
  - https://www.rfc-editor.org/rfc/rfc7592
  - https://www.rfc-editor.org/rfc/rfc7591
  - https://openid.net/specs/openid-connect-registration-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client configuration management

Goal: manage client lifecycle without admin consoles.

Method (RFC 7592): call the client configuration endpoint with the `registration_access_token` as a bearer token. GET (read) returns the current registration, with HTTP 200; PUT (update) replaces the client's metadata: values in the request replace the old ones and omitted fields are treated as null or empty, i.e. deleted, so send the full set; DELETE removes the client and the server answers 204 No Content. In read and update responses values such as `client_secret` and `registration_access_token` MAY differ from the earlier ones; if a new secret or token is returned, the client MUST immediately discard the old one.

Gotchas:
- The update request MUST NOT include `registration_access_token`, `registration_client_uri`, `client_secret_expires_at` or `client_id_issued_at`, and the `client_id` MUST NOT change from the initial registration.
- A missing or invalid registration access token gets HTTP 401.
- Treat the registration access token as a secret credential.

Verify: update `client_name` and read it back; delete the client and confirm the old registration token is rejected.

## Checked

Date: 2026-11-02. Confirmed in RFC 7592 (read, update, delete, 204, 401, client_id immutability, omitted fields, token and secret replacement) and the OpenID Connect Dynamic Client Registration page (`registration_access_token`). Removed as not stated there: read-only-field ignore-or-reject wording, expiring unused dynamic clients, the claim that many IdPs implement RFC 7592 only partly.

Method: documentation only; no commands were run.
