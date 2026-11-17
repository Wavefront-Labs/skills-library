---
id: computing-software.cloud-infrastructure-engineering.terraform.sensitive-variables-in-plans-outputs-and-errors
name: sensitive-variables-in-plans-outputs-and-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, sensitive-variable-masking, sensitive-variable, sensitive-values, outputs]
level: practitioner
status: docs-checked
description: "What sensitive = true hides and what it does not: CLI and plan output, state and plan files, terraform output -json, for_each limits, and ephemeral values."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output", "https://developer.hashicorp.com/terraform/language/values/outputs#sensitive-suppressing-values-in-cli-output", "https://developer.hashicorp.com/terraform/language/state/sensitive-data", "https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive variables: what is masked

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

## Masked
- Terraform redacts the value from CLI output and the HCP Terraform UI.
- Any expression that references a sensitive variable or output is treated as
  sensitive too. A resource argument such as `password = var.database_password`
  shows as `+ password = (sensitive value)` in the plan.
- A sensitive output shows as `connection_string = (sensitive value)` in the apply
  summary, and `terraform output NAME` shows `<sensitive>`.

```hcl
output "connection_string" {
  value     = "postgresql://${var.db_username}:${var.database_password}@${aws_db_instance.main.endpoint}/mydb"
  sensitive = true
}
```

## NOT masked
- The state file: Terraform still stores the values of sensitive variables and
  outputs in state, and local state is a plaintext file.
- Saved plan files: they also hold the values, and the plan page says sensitive data
  is saved in cleartext in the plan file even when the terminal output hides it.
  Anyone who can read state or plan files can read the secret.
- `terraform output -json` and `terraform output -raw` display sensitive outputs in
  plain text.

## Restrictions
- Sensitive values cannot be used as `for_each` arguments: Terraform uses the value
  to identify the instance and always discloses it in UI output, so it returns an
  error. To iterate over a map whose values are sensitive but whose keys are not, the
  for_each page suggests `toset([for k,v in local.map : k])`.

## Patterns
- To keep the value out of state and plan files, add `ephemeral = true` to the
  variable (Terraform 1.10 or later) and pass it only to ephemeral contexts such as
  provider configuration, locals or write-only arguments (Terraform 1.11 or later).
  Combining `sensitive = true` with `ephemeral = true` also redacts it in the CLI
  and UI. Ephemeral cannot be set on root module outputs.
- Secure the state when it holds secrets: store it remotely, encrypt it at rest,
  restrict access and keep audit logs. Exclude local state and any variable
  definition files with secrets from version control.

## Checked
Date: 2026-11-07
Read in full: the Manage sensitive data page (requirements, Hide sensitive variables
and outputs, ephemeral and write-only sections, state security), the Input
variables page (Sensitive values in variables, variable definition files), the Use
outputs page (Sensitive values in outputs), the for_each limitations on values
section and the terraform plan Out option text.
Removed because the pages do not state them: the claim that error messages and
validation messages are redacted, `terraform console` behaviour, the
"Output refers to sensitive values" error and the rule that dependent outputs must
be marked, provider debug logs, `local-exec`, `nonsensitive()` advice, CI secret
masking and the Verify checklist.
Method: documentation only; no commands were run.
