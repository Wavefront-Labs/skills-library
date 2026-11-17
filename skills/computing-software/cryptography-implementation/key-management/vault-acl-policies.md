---
id: computing-software.cryptography-implementation.key-management.vault-acl-policies
name: vault-acl-policies
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, vault-policy, hashicorp-vault, acl, kv-v2, least-privilege, templated-policies, secrets-manager]
level: practitioner
status: docs-checked
description: "Write and test HashiCorp Vault ACL policies: KV v2 data/metadata paths, capabilities, deny precedence, templated identity paths and capability checks."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/policies", "https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2", "https://developer.hashicorp.com/vault/tutorials/policies/policy-templating"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault ACL policies

## Basics
```hcl
# orders-read.hcl
path "secret/data/orders/*" {
  capabilities = ["read"]
}
path "secret/metadata/orders/*" {
  capabilities = ["list", "read"]
}
```
```
vault policy write orders-read orders-read.hcl
```

## KV v2 path gotcha
The CLI path `secret/orders/db` maps to API paths `secret/data/orders/db` (values), `secret/metadata/...` (list,
versions), `secret/delete/`, `secret/undelete/`, `secret/destroy/`. Policies must use the API paths. Listing needs
`list` on the `/metadata/` path even if all other access goes through `/data/`.

## Capabilities
`create`, `read`, `update`, `patch`, `delete`, `list`, `recover`, `sudo`, `deny`. `deny` always takes precedence over
every other capability, including `sudo`. `sudo` is needed for root-protected paths. `+` matches within a single path
segment, `*` is a glob at the end of a path. Wildcards or globs in the rendered output of identity templates give
"permission denied".

## Templated policies
```hcl
path "secret/data/users/{{identity.entity.name}}/*" {
  capabilities = ["create", "read", "update", "delete"]
}
```
Use identity entity names so one policy serves every user or workload.

## Checked

2026-11-01. Confirmed against the Vault policies concepts page (capability list, `deny` precedence, `sudo`, `+` and `*`,
templating limits, `default` policy), the KV v2 API page (`data`, `metadata`, `delete`, `undelete`, `destroy` paths, list on
`metadata`) and the policy-templating tutorial (`identity.entity.name`). Removed: transit examples, `vault token
capabilities`, the `sys/` escalation claim and the claim that `secret/orders/*` grants nothing.
Method: documentation only; no commands were run.

## Review checklist
- No `sudo` except for operators.
- Separate policies for read and write; humans get write, workloads get read.
- `default` policy reviewed (it cannot be removed and is attached to all tokens unless excluded at token creation by
  supporting auth methods).

## Verify
- [ ] Integration test: workload token fails to read another team's path.
