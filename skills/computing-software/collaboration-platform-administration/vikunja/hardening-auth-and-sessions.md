---
id: computing-software.collaboration-platform-administration.vikunja.hardening-auth-and-sessions
name: hardening-auth-and-sessions
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, sso-only, change-status-disable, session-lifetime, jwtttlshort, totp-limits, ldaps-no-starttls]
level: advanced
status: docs-checked
description: "Tighten Vikunja authentication and session lifetimes: SSO-only mode, disabling accounts, LDAPS port settings, TOTP limits and the three JWT TTL options."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/security-hardening.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authentication:
- Prefer OpenID Connect or LDAP. Vikunja creates an account for every user who completes OIDC login, so restrict who may sign in at the identity provider.
- When all users come from SSO set `auth.local.enabled: false` and `service.enableregistration: false`. Disable unneeded local accounts with `vikunja user change-status <id> --disable`.
- LDAP: `auth.ldap.usetls` (default true) means LDAPS with implicit TLS; StartTLS is not supported. `port` defaults to 389, so set your LDAPS port, usually 636. Keep `verifytls` true. The bind account needs read access only.
- TOTP is available to local accounts while `service.enabletotp` is true; it is not enforced and not available to LDAP or OIDC users. Enforce MFA at the identity provider.

Sessions (seconds):
- `service.jwtttlshort` 600: access token lifetime, renewed via refresh token. Ending a session or disabling a user leaves the current access token valid until it expires.
- `service.jwtttl` 259200: inactivity timeout; also link share token lifetime.
- `service.jwtttllong` 2592000: same for "Stay logged in".

Sessions have no absolute maximum if they keep being used. Users can end sessions in settings. Stricter example: 300 / 28800 / 28800.

## Checked

2026-11-04. Confirmed against the Vikunja Security hardening page (setup/security-hardening): OIDC account creation, SSO-only keys, change-status, LDAP over TLS settings, TOTP behaviour, and the three JWT TTL options with defaults and the stricter example. Nothing removed.

Method: documentation only; no commands were run.
