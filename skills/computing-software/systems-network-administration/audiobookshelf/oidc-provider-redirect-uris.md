---
id: computing-software.systems-network-administration.audiobookshelf.oidc-provider-redirect-uris
name: oidc-provider-redirect-uris
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [oidc, sso, redirect-uri, identity-provider, mobile]
level: advanced
status: docs-checked
description: "Register the four Audiobookshelf redirect URIs in your OIDC provider and set Allowed Mobile Redirect URIs for apps."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/oidc-authentication.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/app.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before enabling OIDC (Single Sign-On), register Audiobookshelf as a client in your provider (Authelia, Keycloak, Google, Microsoft or another OIDC-compatible service). Add these redirect URIs:

```text
https://<your.server.com>/auth/openid/callback
https://<your.server.com>/auth/openid/mobile-redirect
https://<your.server.com>/audiobookshelf/auth/openid/callback
https://<your.server.com>/audiobookshelf/auth/openid/mobile-redirect
```

The callback handles web authentication and the mobile-redirect handles mobile app authentication. Both the root path and the `/audiobookshelf` path are supported, so you may need all four depending on your setup.

For mobile apps, add each app's redirect URI to the server's **Allowed Mobile Redirect URIs** field in Audiobookshelf; you do not add those to the OIDC provider. The official app's URI, `audiobookshelf://oauth`, is included by default.

Developer rule from the app FAQ: a third-party app that supports OIDC must use its own unique redirect URI and must not use `audiobookshelf://oauth`.

## Checked

Method: docs-checked 2026-11-09 against the OIDC Authentication page and the App FAQ page (client app rules) of the Audiobookshelf docs repo, both read in full from raw markdown.
