---
id: computing-software.cybersecurity-defensive.authelia.oidc-token-lifespans
name: oidc-token-lifespans
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, token-lifespan, access-token, refresh-token, id-token, custom-lifespan]
level: advanced
status: docs-checked
description: "Set Authelia OIDC token lifespans globally and per client with named custom lifespans, following the documented precedence."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global defaults live under `identity_providers.oidc.lifespans`.

```yaml
identity_providers:
  oidc:
    lifespans:
      access_token: '1h'
      id_token: '1h'
      refresh_token: '90m'
      authorize_code: '1m'
      device_code: '10m'
      custom:
        short_lived:
          access_token: '10m'
          id_token: '10m'
    clients:
      - client_id: '<CLIENT_ID>'
        lifespan: 'short_lived'
```

- `access_token`, `id_token`, `refresh_token`, `authorize_code` and `device_code` are the default maximum lifetimes. The documentation recommends staying near the defaults and using refresh tokens.
- A good refresh token lifespan is 50 percent more, or 30 minutes more (whichever is less), than the longest of the access token and ID token lifespans. With the 60-minute defaults that gives 90 minutes.
- `custom` defines named lifespans. A client selects one with its `lifespan` field. The key under `custom` is the lifespan name.
- Custom lifespans can be set by token type alone or by token type for each grant type. A missing value falls back down the tree: custom by token type and grant, then custom by token type, then the global default.

Check: decode an issued ID token and confirm the `exp` claim matches the lifespan for that client.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider and Clients configuration pages (lifespans defaults, refresh token guidance and 90 minute example, device_code, custom lifespans, grants precedence tree, client lifespan field). Removed: an unsourced recommendation to shorten lifespans for powerful scopes.

Method: documentation only; no commands were run.
