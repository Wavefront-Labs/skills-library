---
id: computing-software.systems-network-administration.apache-guacamole.mfa-overview-sso
name: mfa-overview-sso
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, mfa, sso, extension-priority, authentication-overview, multi-factor-authentication, single-sign-on, auth-extensions]
level: intro
status: docs-checked
description: "Choose between Guacamole's MFA extensions (Duo, TOTP) and SSO (CAS, OpenID Connect, SAML, certificates); control login with extension-priority."
sources:
  - https://guacamole.apache.org/doc/gug/mfa.html
  - https://guacamole.apache.org/doc/gug/sso.html
  - https://guacamole.apache.org/doc/gug/cas-auth.html
  - https://guacamole.apache.org/doc/gug/duo-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFA and SSO overview

MFA extensions:
- **Duo**: proprietary, mobile app (apache-guacamole.duo-mfa).
- **TOTP**: open standard, any authenticator app (apache-guacamole.totp-mfa).
If you use SSO, you can require MFA at the SSO provider instead of a Guacamole MFA extension; Guacamole's Duo support cannot currently be used alongside SSO (use the provider's Duo integration or TOTP).

SSO options:
- CAS (apache-guacamole.cas-sso)
- OpenID Connect (apache-guacamole.openid-connect-sso) and SAML (apache-guacamole.saml-sso): open standards for commercial IdPs (OIDC is not OAuth)
- Smart cards / certificates via SSL/TLS client authentication through a reverse proxy (apache-guacamole.smart-card-ssl-auth)

Login screen (extensions are loaded and evaluated in priority order):
- `extension-priority: <ns>` (the CAS page's example is `cas`) gives the SSO extension priority, so unauthenticated users are redirected straight to the identity provider with no Guacamole login screen.
- `extension-priority: *, <ns>` leaves the SSO extension without priority: a normal login screen with links to the SSO provider(s).
- Default priority is by extension filename, earlier alphabetical first; it can be overridden with `extension-priority`.

Related: apache-guacamole.database-auth-overview, apache-guacamole.header-auth, apache-guacamole.json-auth, apache-guacamole.radius-auth.

Verify: with the chosen priority string, an incognito visit behaves as intended (redirect vs form).

## Checked

2026-11-08. Read the whole of mfa.html and sso.html, the "Controlling login behavior" section of cas-auth.html (partial read) and the Duo and SSO sentence in duo-auth.html (partial read via search). Confirmed the MFA and SSO method descriptions, the OpenID Connect versus OAuth hint, extension-priority behaviour and examples, filename-based default priority, and that Duo cannot be used alongside SSO. Removed the claims that startup logs show namespaces, the openid and saml namespace names, and the sentence that SSO and MFA only authenticate (none on the cited pages).
Method: documentation only; no commands were run.
