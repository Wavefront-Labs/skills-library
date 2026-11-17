---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-policy-templating
name: vault-policy-templating
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, templated-policies, identity-templating, entity-alias]
level: practitioner
status: docs-checked
description: "Write one Vault policy that adapts per entity using identity templating, so teams get isolated paths without a policy per user."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/policies", "https://developer.hashicorp.com/vault/docs/auth/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Templated policies insert identity values into path rules at request time.

```hcl
path "secret/data/{{identity.entity.id}}/*" {
  capabilities = ["create", "update", "patch", "read", "delete"]
}
path "secret/metadata/{{identity.entity.id}}/*" {
  capabilities = ["list"]
}
path "secret/data/{{identity.entity.aliases.auth_kubernetes_xxxx.metadata.service_account_namespace}}/*" {
  capabilities = ["read"]
}
```

Template parameters:
- `identity.entity.id`, `identity.entity.name`, `identity.entity.metadata.<metadata key>`
- `identity.entity.aliases.<mount accessor>.id`, `.name`, `.metadata.<key>`, `.custom_metadata.<key>`
- `identity.groups.ids.<group id>.name`, `identity.groups.ids.<group id>.metadata.<key>`
- `identity.groups.names.<group name>.id`, `identity.groups.names.<group name>.metadata.<key>`

`{{identity.groups.names}}` alone is not a valid parameter; name a group and field.

- Get the mount accessor for the alias form from `vault auth list`.
- If a rendered value contains wildcard characters (`+`, `*`), access is denied. The `deny_slash_in_templated_paths` setting controls how slashes in rendered values are handled.
- Prefer IDs over names where possible, since the policies page notes names can be changed.
- The Kubernetes alias metadata `service_account_namespace` is the example on the Kubernetes auth page for namespace-scoped paths.

## Checked
2026-11-03. Confirmed on the Policies concepts page (parameter list, wildcard denial, `deny_slash_in_templated_paths`, ID preference, mount accessor, KV v2 examples) and the Kubernetes auth page (alias metadata `service_account_namespace`). Fixed: `{{identity.groups.names}}` is not valid, replaced with the documented group forms. Removed: the `vault policy fmt` claim, the empty-value-grants-broader claim, the entity-less token claim, the Verify step and the CI paragraph.
Method: documentation only; no commands were run.
