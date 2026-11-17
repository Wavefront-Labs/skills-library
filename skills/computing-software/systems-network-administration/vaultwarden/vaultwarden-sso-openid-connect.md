---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-sso-openid-connect
name: vaultwarden-sso-openid-connect
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, sso, openid-connect, oidc, sso-authority, pkce, keycloak, authentik, identity-provider]
level: advanced
status: docs-checked
description: "Enable Vaultwarden SSO with OpenID Connect: SSO_AUTHORITY, client credentials, scopes, PKCE, master password reality, callback URL and provider limitations."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Enabling-SSO-support-using-OpenId-Connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden SSO (OpenID Connect)

Core variables: `SSO_ENABLED`, `SSO_AUTHORITY` (the discovery base without `/.well-known/openid-configuration`; it must exactly match the `issuer` in that JSON), `SSO_CLIENT_ID`, `SSO_CLIENT_SECRET`. The callback URL is generated from `DOMAIN`: `/identity/connect/oidc-signin`.

Other settings:

- `SSO_ONLY`: disables email and master-password login.
- `SSO_SIGNUPS_MATCH_EMAIL` (default `true`): link an SSO signup to an existing account with the same email.
- `SSO_SCOPES`: default `profile email` (`openid` implicit). Providers that issue refresh tokens typically want `openid profile email offline_access`; without a refresh token the session is limited to the access-token lifetime.
- `SSO_PKCE` (default `true`); older Zitadel versions may need `false`.
- `SSO_MASTER_PASSWORD_POLICY` is optional; `enforceOnLogin` is unsupported.

A master password is still required and is not controlled by the SSO. Users are linked by an `{iss}/{sub}` identifier in the `sso_users` table, so changing provider means `TRUNCATE TABLE sso_users;`. Send the display name as the `preferred_username` claim to show account names. For a private CA, add the root certificate to `/etc/ssl/certs` or set `SSL_CERT_DIR`/`SSL_CERT_FILE`.

Limitations: Auth0 needs a build with the `oidc-accept-rfc3339-timestamps` feature; signup fails when the provider reports an unverified email (`SSO_ALLOW_UNKNOWN_EMAIL_VERIFICATION` bypasses it but with `SSO_SIGNUPS_MATCH_EMAIL` risks account takeover); Slack needs `SSO_AUTH_ONLY_NOT_SESSION=true`.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Enabling-SSO-support-using-OpenId-Connect.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
