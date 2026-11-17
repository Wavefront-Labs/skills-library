---
id: computing-software.cybersecurity-defensive.dex.dex-refresh-tokens-and-rotation
name: dex-refresh-tokens-and-rotation
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [refresh-tokens, offline-access, rotation, tokens]
level: practitioner
status: docs-checked
description: "Request Dex refresh tokens with offline_access, and know that each refresh issues a new token through refresh token rotation."
sources:
  - https://dexidp.io/docs/configuration/tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A refresh token lets a client obtain a new ID token when the current one expires. Issuing one is optional and happens only when the client passes the `offline_access` scope to Dex.

Example response:

```json
{
  "access_token": "eyJhbGciOiJSUzI1N...",
  "token_type": "Bearer",
  "refresh_token": "lxzzsvasxho5exvwkfa5zhefl",
  "expires_in": 3600,
  "id_token": "eyJhbGciO..."
}
```

Rotation: for every refresh of an ID token Dex issues a new refresh token. This is called refresh token rotation and limits the value of a stolen token.

Gotchas:

- Some connectors do not support `offline_access`. Check the connectors list to see which support refresh tokens before promising long sessions.

Tune lifetimes with the `expiry.refreshTokens` settings described in the expiry skill.

## Checked

2026-11-08: Read the Dex Tokens page in full. Confirmed the refresh token purpose, offline_access, the example response, rotation on every refresh and the connector caveat. Removed connector-specific claims (SAML, authproxy, GitHub, GitLab, Microsoft, OIDC groups) and the request check, which that page does not state.
Method: documentation only; no commands were run.
