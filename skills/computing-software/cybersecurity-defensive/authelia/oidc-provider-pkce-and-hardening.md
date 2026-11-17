---
id: computing-software.cybersecurity-defensive.authelia.oidc-provider-pkce-and-hardening
name: oidc-provider-pkce-and-hardening
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, pkce, par, pushed-authorization-requests, parameter-entropy, hardening]
level: advanced
status: docs-checked
description: "Harden Authelia's OIDC provider with enforce_pkce, parameter entropy, PAR enforcement and signed discovery settings."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Provider-wide options set a security floor that clients can raise.

```yaml
identity_providers:
  oidc:
    enforce_pkce: 'always'
    minimum_parameter_entropy: 8
    enable_pkce_plain_challenge: false
    require_pushed_authorization_requests: false
```

- `enforce_pkce` is `never`, `public_clients_only` (default) or `always`. The default requires PKCE for public clients using the authorization code flow; `always` requires it for every client. Setting `never` is discouraged since it can expose mobile and single-page applications to code interception.
- A single client can require it with `require_pkce`, and choose the method with `pkce_challenge_method`.
- `enable_pkce_plain_challenge` allows the `plain` method; applications should use `S256`.
- `minimum_parameter_entropy` is the minimum length of `nonce` and `state`. `-1` disables validation. Pushing clients to send adequate values is better than lowering it.
- `require_pushed_authorization_requests` forces PAR for all clients; a client can opt in with its own option. Most clients do not support it because it needs a special flow.
- `enable_jwt_access_token_stateless_introspection` allows introspecting JWT access tokens without revocation checks, strongly discouraged. It needs a client with an access token signing algorithm or key ID.
- `discovery_signed_response_alg` signs the discovery metadata. Many clients ignore it and it costs performance, so leave it unset unless needed.
- `enable_client_debug_messages` sends extra debug detail to clients.

Check: attempt an authorization request without a PKCE challenge from a public client and confirm it is rejected.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider and Clients configuration pages (enforce_pkce values and default, enable_pkce_plain_challenge, minimum_parameter_entropy and -1, require_pushed_authorization_requests and the client-level options require_pkce, pkce_challenge_method, stateless introspection prerequisites, discovery_signed_response_alg cost note, enable_client_debug_messages). Removed: nothing.

Method: documentation only; no commands were run.
