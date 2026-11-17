---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-password-policies
name: vault-password-policies
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, password-policies, password-policy, charset]
level: practitioner
status: docs-checked
description: "Write Vault password policies with length and charset rules, test them with the generate endpoint, and attach to supporting engines."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/password-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Password policies control how secrets engines generate passwords. They are unrelated to ACL policies.

```hcl
length = 24
rule "charset" { charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" min-chars = 1 }
rule "charset" { charset = "!@#%^*-_" min-chars = 1 }
```

```sh
vault write sys/policies/password/app policy=@pw.hcl
vault read sys/policies/password/app/generate
```

Gotchas: the minimum length is 4 and at least one charset rule is required; the combined charset is capped at 256 characters. The more restrictive the policy, the longer generation takes; time a policy with the generate endpoint. Vault also tries to generate passwords from a policy before saving it, which catches policies that cannot be satisfied.

## Checked

2026-11-03. Confirmed against the Vault password policy concepts page and the system/policies-password API page (developer.hashicorp.com): parameters, defaults, constraints and examples. Removed: the `database/config` example, the engine-support and database-character claims, the Verify step and the closing advice about non-production namespaces and existing passwords (not on those pages).

Method: documentation only; no commands were run.
