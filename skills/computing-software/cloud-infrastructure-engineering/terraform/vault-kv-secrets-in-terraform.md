---
id: computing-software.cloud-infrastructure-engineering.terraform.vault-kv-secrets-in-terraform
name: vault-kv-secrets-in-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, vault-kv, vault-generic-secret, vault-provider, kv-v2, secrets-management, ephemeral-resource]
level: practitioner
status: docs-checked
description: "Read and write Vault KV v2 secrets from Terraform: provider auth, kv_secret_v2 data vs ephemeral resources, write-only data_json_wo, and keeping secrets out of state."
sources: ["https://registry.terraform.io/providers/hashicorp/vault/latest/docs", "https://registry.terraform.io/providers/hashicorp/vault/latest/docs/data-sources/kv_secret_v2", "https://registry.terraform.io/providers/hashicorp/vault/latest/docs/ephemeral-resources/kv_secret_v2", "https://registry.terraform.io/providers/hashicorp/vault/latest/docs/resources/kv_secret_v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault KV secrets in Terraform

## Provider auth
```hcl
provider "vault" {
  address = "https://vault.example.com"   # or VAULT_ADDR
  # token from VAULT_TOKEN, or:
  auth_login_jwt {
    role  = "terraform-ci"
    mount = "jwt-github"                  # JWT auth mount
  }
}
```
Leave `skip_child_token` at its default; the provider docs discourage setting it to `true`.

## Reading
Ephemeral (value is not stored in state):
```hcl
ephemeral "vault_kv_secret_v2" "api" {
  mount = "kv"
  name  = "prod/payments/api"
}
# ephemeral.vault_kv_secret_v2.api.data["api_key"] - use only where ephemeral values are allowed
```
- `mount` and `name` are required; `version` is optional.
- `name` excludes the mount and the `data` prefix: a secret at `kvv2/data/foo/bar/baz` has name `foo/bar/baz`.
- Optional `mount_id` defers provisioning the ephemeral resource until apply; set it to a mount resource's id when that mount is created in the same configuration.
- Ephemeral resources need Terraform 1.10 or later (the `ephemeralasnull` docs note v1.10 for the ephemeral feature set).

Classic data source (secret is written to state in cleartext):
```hcl
data "vault_kv_secret_v2" "api" {
  mount = "kv"
  name  = "prod/payments/api"
}
```
`vault_generic_secret` is the older generic data source (`path` required). Prefer the kv_v2 ones.

## Writing secrets
```hcl
resource "vault_kv_secret_v2" "db" {
  mount                = "kv"
  name                 = "prod/payments/db"
  data_json_wo         = jsonencode({ password = var.db_password })  # write-only, not read back
  data_json_wo_version = 1
}
```
- `data_json` or `data_json_wo` is required (one of them). `data_json_wo` is write-only and not read from the API; bump `data_json_wo_version` to push a new value.
- `cas` is required when `cas_required` is set on the secret or engine; it must equal the current version.
- `delete_all_versions = true` permanently deletes all versions on destroy.
- `disable_read = true` turns off reading from Vault, so drift is not detected.
- The resource's `data` attribute is deprecated; read back with the ephemeral resource.
- Capabilities needed on the path: create or update, delete (on removal) and read (drift detection).

## Gotchas
- KV v2 API and policy paths contain `/data/`; `name` does not.
- A data source read makes every plan depend on Vault availability and puts the secret in state.
- A long-lived `VAULT_TOKEN` in CI is a standing credential; prefer JWT/OIDC login.

## Verify
- [ ] The secret value does not appear in the state file when using ephemeral and write-only arguments.
- [ ] The Terraform policy grants only the capabilities listed above on its own path.

## Checked
2026-11-09. Confirmed against the Vault provider index (`VAULT_ADDR`, `VAULT_TOKEN`, `auth_login_jwt` with `mount` and `role`, `skip_child_token`), the ephemeral `vault_kv_secret_v2` page (arguments, `name` rule, `mount_id`), the `vault_kv_secret_v2` resource page (`data_json_wo`, `data_json_wo_version`, `cas`, `delete_all_versions`, `disable_read`, deprecated `data`, required capabilities) and the data source page (secret stored in state).
Removed as unconfirmed: the example policy HCL block, the stated `skip_child_token` default text, the `random_password` example, the `terraform state pull` grep check and the audit-log check. The Terraform 1.10 requirement is inferred from a v1.10 note on a Terraform function page, not a dedicated ephemeral-resources page.
Method: documentation only; no commands were run.
