---
id: computing-software.cloud-infrastructure-engineering.openbao.jwt-oidc-auth
name: jwt-oidc-auth
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, jwt, oidc, bound-claims, redirect-uri]
level: advanced
status: docs-checked
description: "OpenBao JWT and OIDC auth: role_type modes, discovery config, bound claims, redirect URI matching and claim_mappings pitfalls."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/auth/jwt/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT and OIDC auth

- `role_type` `jwt`: verify a supplied JWT's signature using static keys, a JWKS URL or OIDC Discovery.
- `role_type` `oidc`: browser login via Authorization Code flow with PKCE, from the UI or CLI.

```
bao auth enable jwt
bao write auth/jwt/config oidc_discovery_url="..." oidc_client_id="..." oidc_client_secret="..." default_role="demo"
bao write auth/jwt/login role=demo jwt=...
bao login -method=oidc port=8400 role=test
```

## Role and config keys

`allowed_redirect_uris`, `bound_audiences` (optional for OIDC), `bound_subject`, `bound_claims` (lists match any item), `user_claim`, `groups_claim`, `claim_mappings`, `oidc_scopes` (e.g. `"profile,groups"`), `oidc_response_mode` (`form_post`), `oidc_disable_confirmation`, `verbose_oidc_logging`.

## Gotchas

- Redirect URIs must match the provider's exactly: scheme, `localhost` vs `127.0.0.1`, port, trailing slash.
- `verbose_oidc_logging` logs claims verbatim; never in production.
- Map-valued parameters like `bound_claims` cannot be set one at a time on the CLI; write the whole role as JSON.
- A `claim_mappings` key starting with `/` must exist in the JWT or auth fails; the metadata key `role` is reserved.
- One verification method per mount; mount another backend at a different path for more.
- Azure users in more than 200 groups need additional configuration.

## Checked

2026-11-04. Read the OpenBao JWT/OIDC auth method overview page in full. Confirmed: role types and verification methods (static keys, JWKS, OIDC Discovery; one per mount), redirect URI rules, the CLI login example, role and config parameter names, map-valued parameters written as one JSON object, the `claim_mappings` leading `/` rule, the reserved `role` metadata key, `verbose_oidc_logging` warning and the Azure 200-group note. Removed: nothing.
Method: documentation only; no commands were run.
