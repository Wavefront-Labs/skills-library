---
id: computing-software.cloud-infrastructure-engineering.terraform.random-password-secrets-manager-and-write-only-arguments
name: random-password-secrets-manager-and-write-only-arguments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, random-password, secretsmanager, write-only-password, write-only-argument, write-only-version, ephemeral-random-password, secrets-in-state]
level: advanced
status: docs-checked
description: "Generate database passwords without leaving them in state: ephemeral random_password, write-only *_wo arguments with *_wo_version, Secrets Manager."
sources: ["https://developer.hashicorp.com/terraform/language/resources/ephemeral/write-only"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passwords: random_password, write-only arguments, Secrets Manager

## Write-only (Terraform 1.11+, provider support required)
Write-only arguments pass temporary values (passwords, API tokens) to a resource without persisting them to state or plan files. They need Terraform v1.11 or later and a resource that supports them; providers indicate in the Registry whether an argument is write-only.
```hcl
ephemeral "random_password" "db" {
  length           = 32
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id                = aws_secretsmanager_secret.db.id
  secret_string_wo         = jsonencode({ username = "app", password = ephemeral.random_password.db.result })
  secret_string_wo_version = 1
}

ephemeral "aws_secretsmanager_secret_version" "db" {
  secret_id  = aws_secretsmanager_secret.db.id
  depends_on = [aws_secretsmanager_secret_version.db]
}

resource "aws_db_instance" "main" {
  password_wo         = jsondecode(ephemeral.aws_secretsmanager_secret_version.db.secret_string)["password"]
  password_wo_version = 1
}
```
- Write-only arguments accept both ephemeral and non-ephemeral values, but HashiCorp recommends using them for ephemeral values. The provider uses the value to configure the resource, then Terraform discards it without storing it in plan or state.
- Terraform cannot diff a value it never stored, and sends write-only arguments to the provider during every operation. Providers typically add a paired `*_wo_version` argument that Terraform does store: **increment it to trigger an update** with the new value. Implementation of the argument and its version argument is provider-specific, so check the Registry page of your provider.
- An ephemeral resource that references a value unknown at plan time (here the secret ID) is deferred to the apply stage.
- In the docs example, the `aws_db_instance` takes `password_wo_version` from `secret_string_wo_version` of the secret version resource, keeping both in step; Azure Key Vault has an equivalent (`value_wo`, `value_wo_version`, `administrator_password_wo`).

## Verify
- [ ] The password does not appear in the state file for the write-only setup (inspect `terraform state pull`).
- [ ] Incrementing the version argument shows an in-place update in the plan.

## Checked
2026-11-08. Read in full: Terraform "Use temporary write-only arguments" page (requirements, version arguments, AWS Secrets Manager and Azure Key Vault examples). Removed: the classic random_password comparison, RDS `manage_master_user_password`, Vault, OpenTofu differences, engine special-character rejection and the claim that moving from `password` to `password_wo` changes nothing, none of which that page states. The registry provider pages were unreadable (empty responses), so provider argument details are not independently confirmed beyond that page. Description trimmed to match.
Method: documentation only; no commands were run.
