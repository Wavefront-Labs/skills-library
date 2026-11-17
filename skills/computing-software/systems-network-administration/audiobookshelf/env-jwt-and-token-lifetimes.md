---
id: computing-software.systems-network-administration.audiobookshelf.env-jwt-and-token-lifetimes
name: env-jwt-and-token-lifetimes
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [environment-variables, jwt, access-token, refresh-token, authentication]
level: practitioner
status: docs-checked
description: "Configure JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRY, REFRESH_TOKEN_EXPIRY and REFRESH_TOKEN_GRACE_PERIOD in Audiobookshelf."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/api-keys.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Security variables that control tokens:

| Variable | Default | Meaning |
| --- | --- | --- |
| `JWT_SECRET_KEY` | random if unset | Secret used to generate JSON Web Tokens. |
| `ACCESS_TOKEN_EXPIRY` | `3600` | Access token lifetime in seconds. |
| `REFRESH_TOKEN_EXPIRY` | `2592000` | Refresh token lifetime in seconds. |
| `REFRESH_TOKEN_GRACE_PERIOD` | `600` | Seconds a just-rotated refresh token is still accepted so concurrent requests during a refresh do not fail. |

If you do not provide `JWT_SECRET_KEY`, a secure random token is generated. Do NOT change it after deployment: if you do, all clients need to reauthenticate.

The API keys page notes that the JWT authentication system arrived in version 2.26.0. Third-party apps should use the standard JWT flow; API keys are meant for server-to-server automation.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Environment Configuration page (Security table) and the API Keys page.

Method: documentation only; no commands were run.
