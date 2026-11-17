---
id: computing-software.ai-ml-engineering.open-webui.set-up-oidc-sso-login
name: set-up-oidc-sso-login
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [sso-oidc, oauth, oidc, google, microsoft, github, persistent-config, open-webui]
level: practitioner
status: docs-checked
description: "Configure Google, Microsoft, GitHub or generic OIDC sign-in for Open WebUI with the right env vars, redirect URIs and token refresh settings."
sources:
  - https://docs.openwebui.com/features/authentication-access/auth/sso/
  - https://docs.openwebui.com/troubleshooting/sso
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let users sign in through an identity provider using environment variables.

## Core variables
- `WEBUI_URL` (public address), `WEBUI_SECRET_KEY` (MUST be set, and shared across a cluster, or sessions and OAuth break).
- `ENABLE_OAUTH_SIGNUP=true` to allow account creation on OAuth login (separate from `ENABLE_SIGNUP`).
- `OAUTH_MERGE_ACCOUNTS_BY_EMAIL=true` merges logins by email (insecure if the provider does not verify email).
- `OAUTH_AUTO_REDIRECT=true` skips the "Continue with SSO" screen; needs exactly one provider, `ENABLE_LOGIN_FORM=false`, no LDAP; `/auth?form=true` still shows the local form.
- `ENABLE_OAUTH_PERSISTENT_CONFIG` defaults to `false`: env vars stay authoritative and Admin Panel > Settings > Authentication shows the OAuth section read-only. Set both it and `ENABLE_PERSISTENT_CONFIG` to `true` to edit in the UI; provider connection changes need a restart of every instance.

## Per provider (redirect URI = `<open-webui>/oauth/<name>/callback`)
- Google: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, callback `/oauth/google/callback`; optional `GOOGLE_OAUTH_AUTHORIZE_PARAMS={"prompt":"consent","hd":"example.com"}`.
- Microsoft (single tenant only): `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`, `MICROSOFT_CLIENT_TENANT_ID` (use `9188040d-6c67-4c5b-b112-36a304b66dad` for personal accounts), optional `MICROSOFT_REDIRECT_URI`.
- GitHub: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, callback `/oauth/github/callback`.
- Generic OIDC (callback `/oauth/oidc/callback`): `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, `OPENID_PROVIDER_URL` (the .well-known/openid-configuration URL, mandatory), `OAUTH_PROVIDER_NAME` (button label, default SSO), `OAUTH_SCOPES` (default `openid email profile`), optional `OPENID_REDIRECT_URI`, `OAUTH_AUDIENCE`, `OAUTH_TOKEN_ENDPOINT_AUTH_METHOD` (`client_secret_basic`, `client_secret_post`, `none`). The `email` claim is required.

## Keep Microsoft sessions alive
```
MICROSOFT_OAUTH_SCOPE=openid email profile offline_access
```
Without `offline_access` there is no refresh token: after about an hour the log shows "No refresh token available for session" and MCP servers with `auth_type: "system_oauth"`, OAuth-authenticated model connections and OneDrive/SharePoint fail (basic chat is unaffected).

## Server-side sessions
Tokens are stored encrypted in the `oauth_session` table; the browser gets an opaque httponly `oauth_session_id` cookie. `OAUTH_MAX_SESSIONS_PER_USER` (default 10) prunes the oldest. Encryption keys default to `WEBUI_SECRET_KEY` (`OAUTH_SESSION_TOKEN_ENCRYPTION_KEY`, `OAUTH_CLIENT_INFO_ENCRYPTION_KEY`).

## Optional extras
`ENABLE_OAUTH_BACKCHANNEL_LOGOUT=true` exposes `POST /oauth/backchannel-logout` (needs Redis to revoke JWTs). `ENABLE_OAUTH_TOKEN_EXCHANGE=true` lets scripts swap an IdP token for a JWT; always set `OAUTH_TOKEN_EXCHANGE_TRUSTED_CLIENT_IDS` (empty = no client check).

## Gotchas
- Only one OIDC provider via `OPENID_PROVIDER_URL`; see the Dual OAuth tutorial for a workaround.
- Nonexistent vars like `OIDC_CONFIG` or `WEBUI_OIDC_CLIENT_ID` do nothing.
- `ENABLE_PROFILE_IMAGE_URL_FORWARDING` leaks client IP to the avatar host; consider `false`.
- Login failing with "Unsupported {'app_id'} in header" means update Open WebUI.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/authentication-access/auth/sso index (read in full). Added the SSO troubleshooting page to sources for the app_id header note. Nothing removed.
Method: documentation only; no commands were run.
