---
id: computing-software.cloud-infrastructure-engineering.zot.bearer-token-authentication
name: bearer-token-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, bearer-auth, token-service, upstream-token-endpoint, access-claims, jwt-verification]
level: advanced
status: docs-checked
description: "Configure Zot HTTP bearer authentication with realm, service and cert, an upstreamTokenEndpoint for combined setups, and per-entry exp in access claims."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
"http": { "auth": { "bearer": {
  "realm": "https://auth.myreg.io/auth/token",
  "service": "myauth",
  "cert": "/etc/zot/auth.crt"
} } }
```

- `realm`, `service`: the token service URL and name.
- `cert`: public key or certificate to verify tokens. Needed for traditional JWT verification unless `awsSecretsManager` or `oidc` is used. Mutually exclusive with `awsSecretsManager`.

Combined with Zot's own token endpoint, add `upstreamTokenEndpoint` (`realm`, `service`) so credentials Zot does not own are forwarded to an external service. Zot-issued API keys, wrapped API-key tokens, workload OIDC tokens and configured OpenID tokens are never forwarded; if they fail, they are rejected. Without it, unrecognised credentials are rejected.

Per-entry expiry: each `access` entry may carry its own `exp`; expired entries are skipped while the token stays valid for others. Omitting `exp` inherits the token-level expiry.

Notes:
- Since v2.1.23, traditional bearer tokens with empty or catalog-only `access` claims grant no repository access to search or other non-catalog routes.
- Traditional bearer tokens cannot match `adminPolicy`.

## Checked

2026-11-04. Read against the zot authn-authz article (HTTP bearer, combined authentication, per-entry expiration); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
