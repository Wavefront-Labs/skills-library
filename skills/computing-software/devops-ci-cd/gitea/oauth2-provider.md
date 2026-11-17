---
id: computing-software.devops-ci-cd.gitea.oauth2-provider
name: oauth2-provider
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-oauth2-provider, gitea, oauth2-pkce, oidc-endpoints, granular-scopes, confidential-client, public-client-loopback, default-applications]
level: advanced
status: docs-checked
description: "Use Gitea as an OAuth2 and OIDC provider: register applications, endpoints, authorization code flow with and without PKCE, scopes and the full-access fallback."
sources: ["https://docs.gitea.com/development/oauth2-provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea as OAuth2 / OIDC provider

Only the **Authorization Code Grant** is supported, plus PKCE and OpenID Connect. Applications are registered by a user (`/user/settings/applications`), an organization admin or an instance admin (`/admin/applications/`). Step 1: name and redirect URL; step 2: Client ID, Client Secret and **Confidential client** flag. The secret shows only once after creation; if lost, regenerate it. The first authorization pops an approval page for the user.

## Endpoints
Discovery `/.well-known/openid-configuration`; authorize `/login/oauth/authorize`; token `/login/oauth/access_token`; introspect `/login/oauth/introspect`; userinfo `/login/oauth/userinfo`; keys `/login/oauth/keys`.

## Scopes
- With only `openid`, `email`, `profile`, `groups` approved, the app gets **full access** to the user's public and private resources. The admin cannot restrict scopes at registration; the third party's request and the user's approval decide.
- Since v1.23 granular scopes work: `read` covers GET routes, `write` covers POST, PUT, PATCH, DELETE too. Adding any PAT scope (`activitypub`, `admin`, `issue`, `misc`, `notification`, `organization`, `package`, `repository`, `user`, each as `read:x` or `write:x`) switches to granular access. `public-only` plus `openid` gives plain SSO (username, email, public org and team membership).
- Adding a scope that is neither OIDC nor a PAT scope falls back to full access. If an app later changes the scopes it requests, the flow fails until re-authorised. `write:package` currently equals `read:package`. No scope at all is not supported.

## Confidential client flow
1. Redirect to `https://HOST/login/oauth/authorize?client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&response_type=code&state=STATE` (state optional, advised against CSRF).
2. POST JSON or form to `/login/oauth/access_token` with `client_id`, `client_secret`, `code`, `grant_type=authorization_code`, `redirect_uri`, which must equal the one in step 1. Response has `access_token`, `token_type` bearer, `expires_in` 3600 and a `refresh_token`.
3. Call the API with the token (see `gitea-api-token`).

## Public client with PKCE
Register as a public client, omit the secret, and send a `code_verifier` (43 to 128 chars of letters, digits, `-`, `.`, `_`, `~`). Authorize with `code_challenge` and `code_challenge_method=S256` (URL-safe base64 of the SHA256 of the verifier) or `plain`; send `code_verifier` in the token request. Loopback redirect URIs like `http://127.0.0.1/` allow any port; avoid `localhost`.

## Preconfigured apps
Gitea creates locked applications at startup (git-credential-oauth, Git Credential Manager, tea); control creation with `DEFAULT_APPLICATIONS` in `app.ini`.

## Checked

2026-11-03: read https://docs.gitea.com/development/oauth2-provider/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Corrected the preconfigured apps list (git-credential-oauth, Git Credential Manager, tea) and removed the unconfirmed `commitstatus` scope.
Method: documentation only; no commands were run.
