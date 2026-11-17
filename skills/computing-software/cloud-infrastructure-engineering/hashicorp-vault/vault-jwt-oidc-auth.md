---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-jwt-oidc-auth
name: vault-jwt-oidc-auth
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, oidc-auth, jwt-auth, oidc]
level: practitioner
status: docs-checked
description: "Set up Vault JWT/OIDC auth with discovery URL, bound audiences, claims and exact redirect URIs for human and CI logins."
sources: ["https://developer.hashicorp.com/vault/docs/auth/jwt", "https://developer.hashicorp.com/vault/api-docs/auth/jwt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JWT auth validates tokens from CI systems or identity providers; OIDC adds the browser login flow for humans.

```sh
vault auth enable oidc
vault write auth/oidc/config oidc_discovery_url="https://idp.example.com" \
  oidc_client_id="vault" oidc_client_secret="<from secret store>" default_role="dev"
vault write auth/oidc/role/dev @role.json
vault login -method=oidc role=dev
```

`role.json` includes `allowed_redirect_uris`, `user_claim`, `bound_audiences`, `policies`, and `bound_claims` (map-valued fields must be written as JSON, not key by key).

Gotchas: redirect URIs must match exactly in Vault and the provider (scheme, host, port, trailing slash, localhost versus 127.0.0.1). Since Vault 1.17, when the JWT in a login request has an `aud` claim, a `jwt` role's `bound_audiences` must exactly match at least one of them; for `oidc` roles `bound_audiences` is optional. Only one JWT signature verification method (`oidc_discovery_url`, `jwks_url` or `jwt_validation_pubkeys`) can be configured per mount. `verbose_oidc_logging` logs received OIDC tokens and claims when debug logging is on and is not recommended in production. A role only requires `user_claim`; start simple and add claim bindings after login works. `vault login -method=oidc` needs a localhost redirect URI such as `http://localhost:8250/oidc/callback`.

## Checked

2026-11-03. Confirmed on the JWT/OIDC auth method and API pages: `auth/oidc/config` with `oidc_discovery_url`, `oidc_client_id`, `oidc_client_secret`, `default_role`; role fields `allowed_redirect_uris`, `user_claim`, `bound_audiences`, `bound_claims`; maps cannot be given key by key on the CLI (`vault write` docs: use a JSON payload); exact-match redirect URIs (http/https, 127.0.0.1/localhost, port, trailing slash); the 1.17 `bound_audiences` rule; one verification method per mount; `verbose_oidc_logging`. Removed: the external-groups remark, the use-another-mount advice and the invented Verify step.

Method: documentation only; no commands were run.
