---
id: computing-software.devops-ci-cd.semaphore-ui.jwt-proxy-authentication
name: jwt-proxy-authentication
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [jwt-proxy, pomerium, jwks, reverse-proxy-auth, authentication, semaphore-ui]
level: advanced
status: docs-checked
description: "Trust a signed JWT header from an authenticating proxy (Pomerium, Cloudflare Access, OAuth2 Proxy) with auth.jwt options."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/jwt-proxy-auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JWT proxy authentication

Goal: sign users in from a JWT added by an authenticating reverse proxy.

Flow: the proxy authenticates the user and adds a signed JWT to a header; Semaphore validates it against the JWKS URL on every request. A valid token finds the user by the external identity for the `sub` claim (provider id `jwt`), else by email depending on `external_auth_email_matching`. A present but invalid token returns 401 immediately; with no header, normal bearer or cookie auth proceeds. A token without `sub` or `exp` is rejected.

```json
{
  "auth": {
    "jwt": {
      "enabled": true,
      "header": "X-Pomerium-Jwt-Assertion",
      "jwks_url": "https://auth.example.com/.well-known/pomerium/jwks.json",
      "audience": "https://semaphore.example.com",
      "issuer": "https://auth.example.com",
      "signout_url": "https://auth.example.com/.pomerium/sign_out"
    }
  }
}
```

Environment: `SEMAPHORE_JWT_AUTH_ENABLED`, `_HEADER`, `_JWKS_URL`, `_AUDIENCE`, `_ISSUER`, `_EMAIL_CLAIM` (default `email`), `_NAME_CLAIM` (default `name`), `_USERNAME_CLAIM` (default `email`), `_SIGNOUT_URL`. `header` and `jwks_url` are required.

Algorithms: ES256/384/512 and RS256/384/512.

Security: make the proxy the only path to Semaphore (private bind or firewall), have it strip the header from client requests, and always set `audience`.

Logout: clearing Semaphore's cookie is not enough; set `signout_url` (Pomerium `/.pomerium/sign_out`, OAuth2 Proxy `/oauth2/sign_out`, Cloudflare `/cdn-cgi/access/logout`).

Verify: a request through the proxy lands signed in; a direct request with a forged header gets 401.

## Checked

2026-11-04: checked against the JWT proxy authentication page. Every claim is stated there.

Method: documentation only; no commands were run.
