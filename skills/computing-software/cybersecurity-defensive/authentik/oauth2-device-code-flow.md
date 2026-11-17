---
id: computing-software.cybersecurity-defensive.authentik.oauth2-device-code-flow
name: oauth2-device-code-flow
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, device-code, device-authorization-grant, oauth2, brand, stage-configuration]
level: practitioner
status: docs-checked
description: "Set up the authentik OAuth2 device code flow: create a Stage Configuration flow, attach it to the brand, and call the device and token endpoints."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/oauth2/device_code/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let input-constrained devices (TVs, printers) obtain user authorization via a second device (RFC 8628).

## Requirements
The active brand must have a device code flow. authentik ships none, so create one:
1. **Flows and Stages > Flows > New Flow**: Name `default-device-code-flow`, Title `Device code flow`, Slug `default-device-code-flow`, **Designation** `Stage Configuration`, **Authentication** `Require authentication`.
2. **System > Brands** > edit the default brand > set **Default code flow** to it > **Update**.

## Initiate
```http
POST /application/o/device/ HTTP/1.1
Host: authentik.company
Content-Type: application/x-www-form-urlencoded

client_id=application_client_id&
scope=openid email my-other-scope
```
The client id may instead go in an `Authorization: Bearer <base64 of client_id:>` header. Response fields: `device_code` (kept on device), `verification_uri`, `verification_uri_complete` (code prefilled), `user_code`, `expires_in`, `interval` (seconds between polls).

## Poll the token endpoint
```http
POST /application/o/token/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:device_code&
client_id=application_client_id&
device_code=device_code_from_above
```
While the user has not finished, the response has `error` = `authorization_pending`; retry after `interval`. On completion you get `access_token` and `id_token` as with any token request.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/oauth2/device_code/.
Nothing was removed.
Method: documentation only; no commands were run.
