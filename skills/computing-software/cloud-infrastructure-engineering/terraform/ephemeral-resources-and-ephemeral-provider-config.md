---
id: computing-software.cloud-infrastructure-engineering.terraform.ephemeral-resources-and-ephemeral-provider-config
name: ephemeral-resources-and-ephemeral-provider-config
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ephemeral-resource, ephemeral-block, write-only-arguments, ephemeralasnull, secrets]
level: advanced
status: docs-checked
description: "Use ephemeral blocks to handle secrets and tokens without storing them in state or plan, plus write-only arguments, ephemeralasnull and lifecycle rules."
sources: ["https://developer.hashicorp.com/terraform/language/resources/ephemeral", "https://developer.hashicorp.com/terraform/language/block/ephemeral", "https://developer.hashicorp.com/terraform/language/functions/ephemeralasnull"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral resources

## What they are
An `ephemeral "<type>" "<name>"` block declares a temporary resource that exists only during the current Terraform operation. Terraform does not store information about ephemeral resources in state or plan files, which suits temporary passwords or connections.

## Pattern from the Terraform docs
```hcl
ephemeral "random_password" "db" {
  length = 32
}

resource "aws_db_instance" "main" {
  # ...
  password_wo = ephemeral.random_password.db.result
}
```
`password_wo` is a write-only argument: it exists only during the current operation and is not saved to state or plan. The docs also show storing a generated password in AWS Secrets Manager through a write-only `secret_string_wo` argument, then reading it back with an ephemeral `aws_secretsmanager_secret_version`. A `*_wo_version` argument tells Terraform when to send a new write-only value.

## Where an ephemeral reference is allowed
Managed-resource write-only arguments, other `ephemeral` blocks, `locals`, variables and child-module outputs declared with `ephemeral = true`, provider configuration, and provisioner and connection settings. Referencing one anywhere else is an error during planning. Ephemeral values in provisioner and connection blocks need Terraform 1.10 or later.

## ephemeralasnull
`ephemeralasnull(v)` (Terraform 1.10 and later, one argument) returns `null` for an ephemeral value and nullifies ephemeral values nested inside an object. The docs' use case: merge a non-ephemeral map with an ephemeral session token and wrap the result, so the output keeps the non-ephemeral keys and shows the token as `null`.

## Lifecycle details
- Terraform opens the ephemeral resource when it needs the result, asks the provider to renew access if the operation outlasts the remote expiry, and closes it after dependent providers finish their work for that phase.
- Ephemeral resources are nodes in the dependency graph. If a resource or data source depends on an ephemeral attribute, the ephemeral resource is provisioned first; if its inputs are unknown until after planning, it is deferred to the apply stage.
- Meta-arguments: `count`, `for_each` (not with `count`), `depends_on`, `provider`, and `lifecycle` with `precondition` and `postcondition` blocks.

## Gotchas
- The provider must ship the ephemeral type; check its registry documentation.
- Because nothing is stored in the plan file, any credentials an ephemeral resource needs must be obtainable again at apply time.

## Verify
- [ ] `terraform state pull` contains no ephemeral resource values.
- [ ] The secret string does not appear in `terraform show -json` of the saved plan.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Terraform ephemeral resources page, ephemeral block reference and ephemeralasnull page. Removed: the Vault and EKS token examples (the provider registry page was not readable), the OpenTofu version claim, the exact error text `Invalid use of ephemeral value`, the "opened during plan and again during apply" detail, and the saved-plan wording (the docs say only that values are not stored in plan files).
