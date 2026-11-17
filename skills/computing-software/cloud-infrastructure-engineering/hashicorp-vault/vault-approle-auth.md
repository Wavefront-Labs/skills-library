---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-approle-auth
name: vault-approle-auth
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, approle-auth, role-id, secret-id]
level: practitioner
status: docs-checked
description: "Configure AppRole for machines with role, secret_id TTL, CIDR binding and response wrapping, and deliver SecretIDs securely."
sources: ["https://developer.hashicorp.com/vault/docs/auth/approle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AppRole splits identity in two: the RoleID (like a username, may be baked into config) and the SecretID (like a password, delivered at runtime).

```sh
vault auth enable approle
vault write auth/approle/role/web token_type=batch token_policies=web \
  secret_id_ttl=10m token_ttl=20m token_max_ttl=30m secret_id_num_uses=1 \
  secret_id_bound_cidrs=10.0.0.0/16
vault read auth/approle/role/web/role-id
vault write -f -wrap-ttl=120s auth/approle/role/web/secret-id
vault write auth/approle/login role_id=<id> secret_id=<secret>
```

Gotchas: deliver SecretIDs through a trusted orchestrator using response wrapping so the plaintext never traverses the CI log. Use `secret_id_num_uses=1` where possible. AppRole is for machines, not humans. If the issued token must create children, set `token_num_uses=0`. User lockout is on by default (5 failures, 15 minutes), which also leaks whether a role exists; configure it deliberately. A custom mount path must appear in the login path.

## Checked

2026-11-03. Confirmed against the Vault AppRole auth method page and its user lockout partial (default threshold 5 attempts, lockout duration 15 minutes, counter reset 15 minutes; may leak existence of accounts; applies to userpass, ldap and approle). Removed: invented verify step and a generic operational-tip paragraph.

Method: documentation only; no commands were run.
