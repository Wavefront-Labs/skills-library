---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oidc-jwt-auth-proxy-and-login-security
name: grafana-oidc-jwt-auth-proxy-and-login-security
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-oauth, keycloak-oidc, oidc-configuration, jwt-authentication, jwt-auth, auth-proxy-setup, header-authentication, brute-force-protection, session-settings]
level: advanced
status: docs-checked
description: "Set up Grafana login via Keycloak (generic OAuth), JWT for embedding, auth proxy headers, and harden brute-force protection, cookies and session lifetimes."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/keycloak/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/jwt/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/auth-proxy/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC, JWT, auth proxy and login security

## Generic OAuth with Keycloak
```ini
[server]
root_url = https://grafana.example.com/     # set so the callback URL is correct, e.g. behind a proxy
[auth.generic_oauth]
enabled = true
name = Keycloak-OAuth
allow_sign_up = true
client_id = YOUR_APP_CLIENT_ID
client_secret = YOUR_APP_CLIENT_SECRET
scopes = openid email profile offline_access roles
email_attribute_path = email
login_attribute_path = username
name_attribute_path = full_name
auth_url = https://<PROVIDER_DOMAIN>/realms/<REALM_NAME>/protocol/openid-connect/auth
token_url = https://<PROVIDER_DOMAIN>/realms/<REALM_NAME>/protocol/openid-connect/token
api_url = https://<PROVIDER_DOMAIN>/realms/<REALM_NAME>/protocol/openid-connect/userinfo
role_attribute_path = contains(roles[*], 'admin') && 'Admin' || contains(roles[*], 'editor') && 'Editor' || 'Viewer'
use_refresh_token = true
signout_redirect_url = https://<PROVIDER_DOMAIN>/realms/<REALM_NAME>/protocol/openid-connect/logout?post_logout_redirect_uri=https%3A%2F%2F<GRAFANA_DOMAIN>%2Flogin
```
- Keycloak client: confidential access type, Standard Flow on, Implicit Flow off, Valid Redirect URIs
  `<grafana_root_url>/login/generic_oauth`. Default client scopes should include `email`, `offline_access`,
  `profile`, `roles`; create the roles `admin`, `editor`, `viewer` and assign them to users.
- `api_url` is not required if the id_token carries all user information, and it can add login latency; it is a
  fallback, or useful beyond 150 group memberships.
- Refresh tokens: add `offline_access` to scopes and `use_refresh_token = true`. Without a refresh token Grafana logs
  the user out when the access token expires.
- Single logout: `signout_redirect_url` as above; Grafana adds `id_token_hint` automatically for OAuth.
- Team sync (Enterprise and Cloud) needs a Group Membership mapper (token claim `groups`, added to ID token) and
  `groups_attribute_path = groups`; the default scopes do not add group claims.
- To grant server admin, return `GrafanaAdmin` from `role_attribute_path` and set `allow_assign_grafana_admin = true`.

## JWT (embedding in another app)
```ini
[auth.jwt]
enabled = true
header_name = X-JWT-Assertion
jwk_set_url = https://idp.example.com/.well-known/jwks.json
username_claim = sub
email_claim = email
expect_claims = {"iss": "https://idp.example.com"}
auto_sign_up = true
role_attribute_path = role
```
- Verification key: exactly one of `key_file`, `key_value`, `jwk_set_file`, `jwk_set_value` or `jwk_set_url`; more than
  one is an error. If the token header carries a `kid`, set `key_id` for key files.
- The `sub` claim is mandatory. By default only `exp`, `nbf` and `iat` are validated; `expect_claims` requires exact
  matches. Grafana does not currently support refresh tokens with JWT.
- JWKS responses are cached for `cache_ttl` (default 60m; `0s` disables).
- Iframe embedding: set `[security] allow_embedding = true` (not available in Grafana Cloud) and have a reverse proxy
  add the JWT header. `url_login = true` reads `auth_token` from the URL when headers cannot be rewritten; the docs warn
  JWTs may be exposed in logs and sessions hijacked without TLS.
- Roles come from the JMESPath `role_attribute_path` (None, Viewer, Editor, Admin); `role_attribute_strict = true`
  denies access if no valid role results; `skip_org_role_sync = true` skips role sync.

## Auth proxy
```ini
[auth.proxy]
enabled = true
header_name = X-WEBAUTH-USER
header_property = username        # or email
auto_sign_up = true
sync_ttl = 15
whitelist = 192.168.1.1, 192.168.1.0/24
headers = Name:X-WEBAUTH-NAME Role:X-WEBAUTH-ROLE Email:X-WEBAUTH-EMAIL Groups:X-WEBAUTH-GROUPS
```
`whitelist` limits where proxy requests may come from to stop users spoofing the header (empty by default). The docs'
Apache example also removes the `Authorization` header before forwarding.

## Login security (`[security]` and `[auth]`)
```ini
[security]
disable_brute_force_login_protection = false   # default; blocked 5 min if attempts are spent in a 5 min window
brute_force_login_protection_max_attempts = 5  # default
cookie_secure = true                           # default false; set when served over HTTPS
cookie_samesite = lax                          # lax (default), strict, none, disabled; OAuth/SAML login needs lax
[auth]
login_maximum_inactive_lifetime_duration = 7d  # default
login_maximum_lifetime_duration = 30d          # default
token_rotation_interval_minutes = 10           # default
disable_login_form = true                      # useful with OAuth 2.0; default false
```

## Verify
- [ ] Login via the IdP works and logout ends the IdP session.
- [ ] Auth proxy only accepts requests from whitelisted proxy addresses.
- [ ] Sessions expire per the configured lifetimes.

## Checked
Checked 2026-11-08 against the Grafana Keycloak, JWT and auth proxy pages and the configuration [security] and [auth]
sections. Removed: `use_pkce`, the `$__file{}` secret syntax and the example IdP hostnames (not on these pages), the
oauth2-proxy and nginx specifics, the advice to set `cookie_samesite = none` for iframes (the page only says OAuth and
SAML need `lax`) and the claim that brute-force lockout is per user.
Method: documentation only; no commands were run.
