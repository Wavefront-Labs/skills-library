---
id: computing-software.cloud-infrastructure-engineering.terraform.secrets-handling-in-state-and-plans
name: secrets-handling-in-state-and-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, secrets, sensitive, state-encryption, external-secrets, plan-json-secrets, nonsensitive, sensitive-variable, state-security, secrets-manager, ephemeral-values, write-only-arguments]
level: advanced
status: docs-checked
description: "Keep real secrets out of Terraform state and plan files: what sensitive=true does and does not do, ephemeral values, write-only arguments, state encryption."
sources: ["https://developer.hashicorp.com/terraform/language/manage-sensitive-data", "https://developer.hashicorp.com/terraform/language/manage-sensitive-data/ephemeral", "https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only", "https://developer.hashicorp.com/terraform/language/functions/nonsensitive", "https://opentofu.org/docs/language/state/encryption/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secrets handling in Terraform state and plans

**Goal:** a leaked state file, plan file or CI log never hands over a usable credential.
That means knowing what `sensitive = true` hides (CLI and HCP Terraform UI output) versus
what it never hides (the value is still stored in state and plan files), and routing real
secrets around state wherever the provider allows.

## 1. What `sensitive` does, and the limit everyone misses
```hcl
variable "database_password" {
  type      = string
  sensitive = true
}
output "connection_string" {
  value     = "postgresql://${var.db_username}:${var.database_password}@${aws_db_instance.main.endpoint}/mydb"
  sensitive = true
}
```
- `sensitive` on `variable` and `output` blocks (Terraform 0.15+) redacts the value in CLI
  output and the HCP Terraform UI, shown as `(sensitive value)`. Expressions that reference a
  sensitive variable or output are treated as sensitive too.
- Terraform still stores these values in **both state and plan files**; anyone who can read
  those files can read the secrets.
- `terraform output -json` and `-raw` print sensitive outputs in plain text.
- Local state is a plaintext file: keep it out of Git. With remote state, Terraform holds it
  in memory only while in use, and you can encrypt it at rest in a backend-specific way.

## 2. Keep the secret out of state: ephemeral values and write-only arguments
- **Terraform 1.10+**: the `ephemeral` argument on variables and child module outputs, and
  the `ephemeral` resource block. Ephemeral values exist at runtime but are omitted from state
  and plan files. You cannot add `ephemeral` to root-module outputs. Ephemeral values may
  only be referenced in `locals`, ephemeral variables and child module outputs, write-only
  arguments, other `ephemeral` blocks, `provider` blocks, and `provisioner`/`connection` blocks.
- **Terraform 1.11+**: write-only arguments on managed resources (usually named `*_wo`, with a
  matching `*_wo_version`). The provider uses the value, then Terraform discards it without
  storing it in state or plan files. Support is defined per provider and resource; check the
  Registry for what your provider offers.
```hcl
variable "api_token" {
  type      = string
  sensitive = true
  ephemeral = true        # both: redacted in the CLI and never stored
}

ephemeral "random_password" "db_password" {
  length = 16
}
resource "aws_db_instance" "example" {
  # ...
  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1
}
```
- Terraform cannot store write-only values, so it cannot detect a change or show a plan diff.
  To trigger an update, increment the `*_wo_version` argument, which Terraform does store.
- Because ephemeral values are not stored, capture any generated value you need later in
  another resource, for example write it to a secrets manager with a write-only argument
  and read it back through an `ephemeral` data source for the consumer. The HashiCorp
  example uses `aws_secretsmanager_secret_version` with `secret_string_wo`.
- Write-only arguments accept non-ephemeral values too, but the docs recommend passing
  ephemeral ones.

## 3. When a secret must be a normal argument
If a resource has no write-only form, the secret lands in state. The docs' mitigations: store
state remotely, encrypt it at rest, restrict who can read it, and keep audit logs of state
access. Treat state read access as secret read access.

## 4. State encryption and access control
- Backend encryption at rest is backend-specific: HCP Terraform encrypts state at rest (and
  lets you supply keys), the S3 backend encrypts when its `encrypt` option is enabled, and the
  GCS backend supports customer-supplied or customer-managed keys. TLS protects it in transit
  for these.
- **OpenTofu** (not Terraform) can encrypt state and plan files themselves, locally or in a
  backend, and for `terraform_remote_state`. Once enabled, state and plan files are
  unrecoverable without the key, so back up the keys and take a temporary backup of the
  unencrypted state first. Its page warns that encryption does not protect against data
  loss or replay of an older state/plan file, and does not protect sensitive values from the
  person running `tofu`. With many people needing state access, run production plan and apply
  from CI to protect the key and the values. Migration uses an `unencrypted` method (to read
  existing plaintext state) and a `fallback` method (tried when reading with the new method
  fails; saves always use the new method).

## Gotchas
- `nonsensitive()` removes the sensitive marking. The docs say to use it only when you derived
  a value that no longer contains the sensitive part (for example a hash, or a non-secret
  fragment of a JSON blob) and to treat each call as deliberate; used loosely, sensitive
  values appear clearly in output.
- `(sensitive value)` redaction is a display feature; anything that reads the state or plan
  JSON directly sees the stored values.

## Verify
- [ ] Every resource argument holding a real secret uses a write-only argument or an
  ephemeral value where the provider supports it, or the exception is documented.
- [ ] State backend access is scoped and audited as tightly as direct secret-manager access.
- [ ] Remote state is encrypted at rest (backend option, or OpenTofu encryption with backed-up keys).
- [ ] Every `nonsensitive()` call has a comment justifying why it is safe there.

## Checked
Checked 2026-11-08 against HashiCorp's Manage sensitive data, ephemeral values, write-only arguments and nonsensitive pages, and the OpenTofu state encryption page.
Corrected: Terraform has no native state/plan encryption in the cited pages (it is OpenTofu), and the prior "ephemeral values: check support" note now names the 1.10 and 1.11 requirements. Removed: Vault provider claims, `lifecycle ignore_changes` advice, `before_sensitive`/`after_sensitive` plan JSON detail, `terraform console` and `TF_LOG=debug` claims, and the older-version propagation bug, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
