---
id: computing-software.cybersecurity-defensive.authelia.oidc-client-registration
name: oidc-client-registration
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, oidc-client, client-id, client-secret, redirect-uris, public-client]
level: practitioner
status: docs-checked
description: "Register an OpenID Connect client in Authelia with client_id, secret, redirect URIs, scopes and the public or confidential client type."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clients live under `identity_providers.oidc.clients`.

```yaml
identity_providers:
  oidc:
    clients:
      - client_id: '<CLIENT_ID>'
        client_name: 'Example App'
        client_secret: '<CLIENT_SECRET>'
        public: false
        redirect_uris:
          - 'https://app.example.com/oauth2/callback'
        scopes:
          - 'openid'
          - 'profile'
          - 'email'
          - 'groups'
```

- `client_id` is 100 characters or fewer, uses only RFC 3986 unreserved characters and is unique across clients. A semi-long random string is recommended.
- `client_secret` is shared with the application and must match. It is required for confidential clients, except when `token_endpoint_auth_method` uses a non-secret credential such as a key. Generate it as described in the FAQ on generating client identifiers and secrets.
- `public: true` suits SPAs and CLI tools that cannot keep a secret, and requires a blank `client_secret`.
- `redirect_uris` is the allowlist of callbacks. A request with an unlisted URI fails. URIs are case-sensitive and must use `http` or `https`.
- `scopes` should be those in the claims documentation. Authelia logs a warning for undocumented scopes unless the client has the `client_credentials` grant, where arbitrary scopes are expected.
- `grant_types` is best left unset unless you know what you are doing.
- `token_endpoint_auth_method` defaults to `client_secret_basic` for confidential clients and `none` for public ones.

Check: complete a login from the application and confirm the token endpoint call succeeds.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Clients configuration page (client_id limits, client_secret rules, public, redirect_uris restrictions, scopes warning, grant_types advice, token_endpoint_auth_method defaults). Removed: a claim about environment variables that the page does not make.

Method: documentation only; no commands were run.
