---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-oidc-authentication
name: bookstack-oidc-authentication
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, oidc, openid-connect, sso, auth-method, discovery, group-sync, pkce, groups-claim]
level: advanced
status: docs-checked
description: "Set up BookStack OpenID Connect login: OIDC_ variables, issuer discovery or manual endpoints, callback and logout URIs, scopes, PKCE, claims and group sync."
sources: ["https://www.bookstackapp.com/docs/admin/oidc-auth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack OIDC authentication

Core: `AUTH_METHOD=oidc`, `OIDC_NAME` (button label, example `SSO`), `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_ISSUER` (must start `https://`), `OIDC_ISSUER_DISCOVER=true` to use discovery, `AUTH_AUTO_INITIATE` for OIDC-only sites.

Without discovery set `OIDC_PUBLIC_KEY` (RSA key path), `OIDC_AUTH_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_USERINFO_ENDPOINT`. Discovery reads `<issuer>/.well-known/openid-configuration` and the JWKS URI.

Register with the provider: login callback `https://example.com/oidc/callback`; logout redirects to the base URL, `/login` and `/login?prevent_auto_init=true`. Default scopes `openid profile email`; add more via `OIDC_ADDITIONAL_SCOPES`. PKCE is used since v24.02. Only RS256 signing is supported; encrypted tokens are not.

Identity: users link by the `sub` claim (`OIDC_EXTERNAL_ID_CLAIM` overrides; changing it breaks existing logins). `OIDC_DISPLAY_NAME_CLAIMS` (example `name`; join several with `|`). `OIDC_FETCH_AVATAR` does server-side fetches, so enable only for trusted providers. `OIDC_END_SESSION_ENDPOINT=true` enables RP-initiated logout.

Group sync: `OIDC_USER_TO_GROUPS=true`, `OIDC_GROUPS_CLAIM=groups` (dot-notation for nesting, e.g. `resource_access.bookstack.roles`), `OIDC_REMOVE_FROM_GROUPS=true`. Names match role names case-insensitively, lowercased with hyphens, or the role's External Authentication IDs.

Switching from standard auth does not match accounts by email: set each user's External Authentication ID while still on `standard`, or update `users.external_auth_id` in bulk. `OIDC_DUMP_USER_DETAILS=true` blocks logins; debug only.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/oidc-auth/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: 'default' labels on OIDC_NAME, OIDC_ISSUER_DISCOVER and OIDC_DISPLAY_NAME_CLAIMS (the page shows them only as example values).
Method: documentation only; no commands were run.
