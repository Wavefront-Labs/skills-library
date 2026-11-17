---
id: computing-software.cybersecurity-defensive.authelia.oidc-cors-configuration
name: oidc-cors-configuration
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, cors, allowed-origins, userinfo, browser-clients]
level: practitioner
status: docs-checked
description: "Enable cross-origin access to chosen Authelia OIDC endpoints and restrict allowed origins, for browser-based clients that call userinfo or token."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some OpenID Connect endpoints must serve CORS headers, and others are optional. Authelia replies with CORS headers whenever the request carries an `Origin` header.

```yaml
identity_providers:
  oidc:
    cors:
      endpoints:
        - 'authorization'
        - 'token'
        - 'revocation'
        - 'introspection'
        - 'userinfo'
      allowed_origins:
        - 'https://app.example.com'
      allowed_origins_from_client_redirect_uris: false
```

- `endpoints` lists the endpoints configured for CORS. Allowed values are `authorization`, `pushed-authorization-request`, `token`, `revocation`, `introspection` and `userinfo`. The documentation recommends including at least `userinfo`.
- `allowed_origins` lists origins with scheme, host and port only, no trailing slash or path. If you do not configure it (and the redirect URI option is off), any `https` origin is permitted. To allow `http` origins you must list them, which is not recommended.
- The single wildcard `*` is allowed but must be the only entry, and `allowed_origins_from_client_redirect_uris` must not be enabled with it.
- `allowed_origins_from_client_redirect_uris: true` derives the allowed origins from each client's redirect URIs.

Check: from the browser console of your app, call `userinfo` with fetch and confirm the response carries `Access-Control-Allow-Origin`.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider configuration page (cors endpoints list, userinfo recommendation, allowed_origins rules and https default, wildcard restrictions, allowed_origins_from_client_redirect_uris). Removed: an unsourced warning about wildcard origins.

Method: documentation only; no commands were run.
