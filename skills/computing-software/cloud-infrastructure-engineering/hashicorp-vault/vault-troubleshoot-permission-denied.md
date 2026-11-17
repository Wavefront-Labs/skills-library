---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-troubleshoot-permission-denied
name: vault-troubleshoot-permission-denied
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, permission-denied, vault-403, token-capabilities]
level: practitioner
status: docs-checked
description: "Trace Vault 403s using token capabilities, token lookup, audit entries and path details (KV v2 data prefix, namespace)."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/policies", "https://developer.hashicorp.com/vault/docs/audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Work through the chain: token, policy, path, namespace.

```sh
vault token lookup                       # policies, ttl, entity, namespace
vault token capabilities secret/data/app/db
vault policy read app
vault read sys/internal/ui/mounts/secret/data/app/db    # shows how the path is resolved
```

Then search the audit log for the failing request path.

Typical causes: KV v2 path missing `data/`; token expired or revoked (`invalid token` rather than `permission denied`); policy not attached to the entity or group; wrong namespace; or a `deny` rule in another policy (`deny` always takes precedence).

Gotchas: grant `list` on the metadata path when a client needs to enumerate keys. Avoid fixing with `*` wildcards; find the exact path in the audit log.

## Checked

2026-11-03. Confirmed against the Vault policies concepts page (deny by default, `deny` precedence, capabilities list) and the tokens page (403 `invalid token` / `permission denied`). Removed: claim about when token policy lists are evaluated, parameter-constraint caveat on capabilities, and an invented verify step. `/sys/internal/ui/mounts` confirmed on its API page.

Method: documentation only; no commands were run.
