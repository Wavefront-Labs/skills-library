---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-policy-writing
name: vault-policy-writing
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, policy-writing, vault-policy, capabilities]
level: practitioner
status: docs-checked
description: "Author Vault policies with correct path globbing, capabilities and KV v2 paths, and apply them with vault policy write."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies are deny by default. A path rule grants capabilities: `create`, `read`, `update`, `patch`, `delete`, `list`, `sudo`, `deny`, `subscribe`, `recover`.

```hcl
path "secret/data/app/*" {
  capabilities = ["read", "list"]
}
path "secret/metadata/app/*" {
  capabilities = ["list"]
}
path "secret/data/app/admin" {
  capabilities = ["deny"]
}
```

```sh
vault policy write app-read app-read.hcl
```

- `*` is a prefix glob and only valid as the last character of a path. `+` matches any characters within a single path segment (since Vault 1.1), for example `secret/+/teamb`.
- When several rules match, the most specific path wins. `deny` always takes precedence.
- KV v2 reads and writes use `secret/data/...`; listing and metadata use `secret/metadata/...`. Grant both when a client needs to list.
- Listing returns keys unfiltered; the page notes you cannot restrict which keys a list returns.
- Generating credentials from a dynamic secrets engine is a `read` request, so `read` on that path grants it.
- `allowed_parameters`, `denied_parameters` and `required_parameters` are not supported for KV v2.

## Checked
2026-11-03. Confirmed on the Policies concepts page (deny by default, capability list, glob and `+` rules, specificity and deny precedence, list behaviour, credential generation as read, parameter constraints and the KV v2 limit, KV v2 `data`/`metadata` examples, `vault policy write`). Removed: the `vault policy read` and `vault token capabilities` lines, the claim that `denied_parameters` pass when the parameter is omitted, and the Verify step.
Method: documentation only; no commands were run.
