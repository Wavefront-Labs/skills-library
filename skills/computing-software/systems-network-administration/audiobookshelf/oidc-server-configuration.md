---
id: computing-software.systems-network-administration.audiobookshelf.oidc-server-configuration
name: oidc-server-configuration
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [oidc, sso, issuer-url, discovery, client-id, jwks]
level: advanced
status: docs-checked
description: "Configure Audiobookshelf OIDC under Settings, Authentication using auto-discovery or the manual endpoint and algorithm fields."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/oidc-authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Go to **Settings, Authentication** and enable **OpenID Connect Authentication**. Only an admin can configure it. Once a user is logged in, the refresh token is authenticated against Audiobookshelf, not the OIDC provider.

Auto-discovery fills most fields from an issuer URL. Examples:

- `https://auth.example.com/application/o/audiobookshelf/`
- `https://auth.example.com/.well-known/openid-configuration`

If discovery fails, set fields manually:

| Field | Meaning |
| --- | --- |
| Issuer URL | Base URL identifying the provider |
| Authorize URL | Where users are redirected to authenticate |
| Token URL | Exchanges authorization codes for tokens |
| Userinfo URL | Returns user profile information |
| JWKS URL | Key set used to verify tokens |
| Logout URL | Ends SSO sessions |
| Client ID / Client Secret | Identify Audiobookshelf to the provider |
| Signing Algorithm | For example RS256 or ES256 |

Test the login fully before disabling local authentication (see the lockout recovery skill).

## Checked

Method: docs-checked 2026-11-09 against the OIDC Authentication page of the Audiobookshelf docs repo, read in full from raw markdown.
