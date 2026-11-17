---
id: computing-software.cybersecurity-defensive.zitadel.refresh-revocation-and-logout
name: refresh-revocation-and-logout
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, refresh-token, revocation, end-session, logout, oidc]
level: practitioner
status: docs-checked
description: "Renew tokens with a refresh token, revoke tokens, and end ZITADEL sessions with the end_session endpoint and a registered redirect."
sources:
  - https://zitadel.com/docs/apis/openidoauth/endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Refresh: to get a new access token without user interaction, use the refresh token grant. Request the `offline_access` scope in the original authorization request. Send `grant_type=refresh_token` and the `refresh_token`. The optional `scope` must be a subset of the originally requested scopes; if omitted, the original scopes are reused.

Revocation: `${CUSTOM_DOMAIN}/oauth/v2/revoke` takes a `token`. Revoking an access token revokes only that token. Revoking a refresh token also revokes its corresponding access token. Clients authenticate as for the token endpoint.

Logout: open `${CUSTOM_DOMAIN}/oidc/v1/end_session` in the user's browser to terminate the user sessions. Optional parameters:

- `id_token_hint`: an ID token previously issued to the client
- `client_id`
- `post_logout_redirect_uri`: must exactly match a URI registered in the console
- `state`
- `logout_hint`: a login name, supported only with login UI V2
- `ui_locales`

ZITADEL checks the logout redirect against the client taken from the `azp` claim of the `id_token_hint` or from `client_id`. If both are given they must be equal. With neither, the redirect is ignored.

Register post-logout URIs in the application and pass `id_token_hint` so users land back in your app.

## Checked
2026-11-08. Confirmed against the ZITADEL OIDC endpoints page: refresh token grant parameters (grant_type refresh_token, scope subset rule, offline_access), revoke endpoint behaviour for access and refresh tokens, end_session parameters including logout_hint (login UI V2 only) and the azp and client_id redirect check.
Method: documentation only; no commands were run.
