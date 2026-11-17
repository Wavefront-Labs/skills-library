---
id: computing-software.web-development.ghost.ghost-admin-api-jwt-token-generation
name: ghost-admin-api-jwt-token-generation
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, jwt, hs256, authorization-header, integration-key]
level: advanced
status: docs-checked
description: "Generate the short-lived HS256 JWT that authenticates Ghost Admin API requests from an id:secret key without the client library."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate to the Admin API from a language without the official client.

An Admin API key is `id:secret`. The id goes in the JWT header, the secret signs the token. Never exchange keys for tokens in a browser or any insecure environment.

Header: `{"alg": "HS256", "kid": "<key id>", "typ": "JWT"}`.
Payload: `{"exp": <timestamp>, "iat": <timestamp>, "aud": "/admin/"}`. Timestamps are seconds since the Unix epoch, not milliseconds. `exp` must be at most 5 minutes after now. The docs say the libraries on jwt.io differ slightly, so follow your library's way of passing the signing secret (the docs example decodes the hex secret first).

Send it as:

`curl -H "Authorization: Ghost $token" -H "Accept-Version: $version" https://{admin_domain}/ghost/api/admin/{resource}/`

Note the scheme is the word `Ghost`, not `Bearer`. The docs describe these as short-lived, single-use tokens, so generate a fresh one per request.

Where possible the API returns specific error messages when required header or payload values are missing or incorrect.

Verify: `GET /admin/posts/?limit=1` with the token returns posts rather than an authentication error.

## Checked

2026-11-04. Confirmed: id:secret key, header and payload fields, seconds not milliseconds, 5 minute maximum, hex secret decoding, the Ghost authorization scheme (Admin API overview page). Removed: the invented "common failures" list and the claim that GET /admin/site/ needs no authentication.

Method: documentation only; no commands were run.
