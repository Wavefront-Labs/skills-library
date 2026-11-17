---
id: computing-software.systems-network-administration.immich.oauth-client-setup
name: oauth-client-setup
category: computing-software
field: systems-network-administration
product: immich
tags: [oauth, oidc, redirect-uri, authentik, keycloak, backchannel-logout]
level: practitioner
status: docs-checked
description: "Create the OIDC client in your identity provider for Immich: client type, grant type, redirect URIs for web and mobile, and backchannel logout."
sources:
  - https://docs.immich.app/administration/oauth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: prepare the identity provider before enabling OAuth in Immich. Immich supports OpenID Connect; examples in the docs include Authentik, Authelia, Okta, Google and Keycloak.

Create a new client application with:

1. Provider type `OpenID Connect` or `OAuth2`.
2. Client type `Confidential`.
3. Application type `Web`.
4. Grant type `Authorization Code`.

Sign-in redirect URIs must cover every domain you use:

- `app.immich:///oauth-callback`: required for the iOS and Android apps.
- `https://immich.example.com/auth/login`: web login.
- `https://immich.example.com/user-settings`: manually linking OAuth from the web client.

Repeat the last two for each access method, for example `http://localhost:2283/...` and `http://192.168.0.200:2283/...`.

If the provider supports it, set the backchannel logout URL to `http://DOMAIN:PORT/api/oauth/backchannel-logout`.

Keycloak specifics from the docs: Issuer URL `https://<KEYCLOAK_DOMAIN>/realms/<YOUR_REALM>`, client secret from Clients, immich, Credentials, and a role claim managed through client roles with a mapper whose claim name is `immich_role`.

The Issuer URL must return a valid JSON discovery document. The `.well-known/openid-configuration` suffix is optional because discovery adds it.

Then enter the issuer, client ID and secret in Administration, Settings, OAuth (see the settings and claims skill). If you get locked out, `immich-admin enable-password-login` restores password sign-in.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/oauth (Overview, Prerequisites, Enable OAuth, Keycloak Example); administration/server-commands (enable-password-login).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
