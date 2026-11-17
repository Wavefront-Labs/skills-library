---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.sensitive-and-ephemeral-values-in-terraform
name: sensitive-and-ephemeral-values-in-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, secrets-in-iac, sensitive-variables, ephemeral-values, terraform, opentofu, write-only-attributes, state-secrets, ephemeral-resources]
level: advanced
status: docs-checked
description: "Handle secrets in Terraform: what sensitive = true does and does not do, ephemeral variables and resources, and write-only arguments."
sources:
  - https://developer.hashicorp.com/terraform/language/values/variables
  - https://developer.hashicorp.com/terraform/language/resources/ephemeral
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive and ephemeral values in Terraform

Goal: secrets used by Terraform are hidden in output and, where possible, never written to plan files or state at all.

## `sensitive = true`: redaction only
```hcl
variable "database_password" {
  type        = string
  description = "Password for the RDS database instance"
  sensitive   = true
}
```
The `sensitive` argument stops Terraform displaying the value in CLI output. Terraform **still stores the values of sensitive variables in state**, so state readers are secret readers.

## Ephemeral variables
Add the `ephemeral` argument to a `variable` block to omit that variable from state and plan files. It adds restrictions on where the value can be used, so Terraform will reject uses that would persist it.

## Ephemeral resources
The `ephemeral` block defines temporary resources, such as a temporary password or a connection to another system. Terraform does not store information about ephemeral resources in state or plan files.
```hcl
ephemeral "random_password" "db_password" {
  length = 16
}
```

## Write-only arguments
Managed resources can have write-only arguments, which are only available during the current operation and are not stored in state or plan files. Terraform sends the value to the provider, which uses it, and Terraform then discards it. A companion `*_version` argument is used alongside, as in this documented example:
```hcl
resource "aws_db_instance" "example" {
  # ...
  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1
}
```
Which resources offer `_wo` arguments depends on the provider; check the resource docs.

## Gotchas
- A variable definition file that holds sensitive values should be ignored in your VCS provider.
- `sensitive` is display redaction only; use ephemeral variables, ephemeral resources or write-only arguments when the value must stay out of state.

## Verify
- [ ] The secret does not appear in state after apply for ephemeral/write-only flows.
- [ ] Remaining sensitive attributes are protected by access control on the state backend.

## Checked
Method: docs-checked 2026-11-09 against the HashiCorp Terraform "input variables" and "ephemeral values in resources" pages (full text read).
Removed: Terraform 1.10/1.11 version numbers, nonsensitive(), terraform output -raw and show -json behaviour, sensitive outputs rule, backend-encryption, OpenTofu encryption, for_each key and TF_LOG gotchas, bumping the _wo version to rotate (not on the pages read).
