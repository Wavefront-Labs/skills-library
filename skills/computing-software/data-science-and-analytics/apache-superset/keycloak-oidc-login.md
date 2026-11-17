---
id: computing-software.data-science-and-analytics.apache-superset.keycloak-oidc-login
name: keycloak-oidc-login
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [keycloak, oidc, pkce, groups-mapper, logout]
level: advanced
status: docs-checked
description: "Wire Superset to Keycloak OIDC: confidential client, PKCE S256, redirect URI, Group Membership mapper to roles, public URL and RP-initiated logout."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/oauth.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: single sign-on from Keycloak with group-driven roles.

Prerequisite: Authlib 1.2 or later in the Superset image (build a custom image rather than installing at startup).

Keycloak side:
1. Create a confidential OIDC client. Valid redirect URI: `https://<superset-host>/oauth-authorized/keycloak`. Valid post logout redirect URIs: the exact value of `SUPERSET_PUBLIC_URL` (mind the trailing slash), or Keycloak rejects the logout redirect.
2. PKCE: set Proof Key for Code Exchange Code Challenge Method to `S256` under Clients, the client, Advanced, Advanced settings.
3. Keycloak does not expose a groups claim by default. Add a Group Membership mapper (Client scopes, the dedicated scope, Add mapper, By configuration) with Token Claim Name `groups`, Full group path OFF (otherwise names arrive as `/name` and role mapping silently fails) and Add to userinfo ON. The ID and access token options can be OFF: groups are read from the userinfo endpoint.
4. Create groups named `<client_id>_admin`, `_alpha`, `_gamma`, `_public` and assign users.

Superset side (`superset_config.py`, example uses a custom security manager):
- `AUTH_TYPE = AUTH_OAUTH`, `AUTH_ROLES_SYNC_AT_LOGIN = True`, `AUTH_USER_REGISTRATION = True`.
- `OAUTH_PROVIDERS` entry with `name: 'keycloak'` (the callback path segment `/oauth-authorized/keycloak` equals this name) and `remote_app` holding `client_id`, `client_secret`, `server_metadata_url` and `client_kwargs` with `scope: 'openid email profile'` and `code_challenge_method: 'S256'`.
- `AUTH_ROLES_MAPPING` maps the group names to roles such as `Admin`, `Alpha`, `Gamma`, `Public`.
- `ENABLE_PROXY_FIX = True` when TLS ends at an ingress or proxy; otherwise the login redirect URI is generated with `http://` and Keycloak rejects it.
- Issuer URL: legacy (Wildfly, before 17) `https://<keycloak-host>/auth/realms/<REALM>`; modern (Quarkus) `https://<keycloak-host>/realms/<REALM>`.

Logout: the example overrides the OAuth view's logout to redirect to `<issuer>/protocol/openid-connect/logout` with `client_id`, `post_logout_redirect_uri` and `id_token_hint` (the ID token stored in the session at login).

Troubleshooting from the page: everyone rejected with "no authorized group" means the mapper is missing or Add to userinfo is off; groups with a leading slash mean Full group path is on; `Invalid parameter: redirect_uri` means the proxy fix is missing or the redirect URI is not registered; `Invalid redirect uri` on logout means `SUPERSET_PUBLIC_URL` differs from the registered post logout URI; `mismatching_state` means the session cookie was lost (check `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_SAMESITE`, and cookie size); 404 on token or auth endpoint means the wrong issuer path for your Keycloak version.

## Checked

2026-11-08. Confirmed against the OAuth Configuration page (Keycloak example, prerequisites, Helm configuration and troubleshooting table, read in full). Removed: the "PKCE only if the client requires it" condition (the page enables S256 unconditionally) and the generic "if login loops" advice (replaced by the page's troubleshooting table).
Method: documentation only; no commands were run.
