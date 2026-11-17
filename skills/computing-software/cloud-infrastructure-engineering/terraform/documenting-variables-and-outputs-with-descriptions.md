---
id: computing-software.cloud-infrastructure-engineering.terraform.documenting-variables-and-outputs-with-descriptions
name: documenting-variables-and-outputs-with-descriptions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, variable-description, output-description, terraform-docs, module-design, documentation]
level: practitioner
status: docs-checked
description: "Write variable and output descriptions that callers can act on: units, allowed values, defaults rationale, and generating module docs from them with terraform-docs."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables", "https://developer.hashicorp.com/terraform/language/values/outputs", "https://terraform-docs.io/user-guide/introduction/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptions for variables and outputs

## Where descriptions are used
- `description` is an argument of both `variable` and `output` blocks.
- When a module variable has no default, Terraform prompts the user for a value before planning; a clear description tells them what to enter.
- terraform-docs "generates documentation from Terraform modules in various output formats"; markdown table is a common format for a module README, and it can be rerun manually, from a pre-commit hook or in CI.

## What a good description contains
```hcl
variable "retention_days" {
  type        = number
  default     = 30
  description = "Days to keep log events. Allowed values are those the log service accepts; see the resource documentation. 0 means never expire."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs for the service network interfaces, at least two in different availability zones."
}

output "security_group_id" {
  value       = aws_security_group.this.id
  description = "ID of the service security group. Add ingress rules to this group to allow callers in."
}
```
Checklist (design guidance): what it is, units, allowed values or format, effect of null or empty, why the default is what it is, and for outputs what the caller should do with it.

## Style (design guidance)
- Full sentences, end with a period; no "The variable for ...".
- Do not restate the type.
- Mark sensitivity in prose only if `sensitive = true` is not obvious.
- Keep it short; link to docs for long explanations.

## Enforce
Run terraform-docs on the module path (`terraform-docs /module/path`), optionally with a `.terraform-docs.yml` for consistent configuration, and in pre-commit or CI so the README does not drift. Missing descriptions can be caught by a linter; check your linter's own documentation for the rule names.

## Verify
- [ ] Every variable and output has a description.
- [ ] README inputs table generated and current.

## Checked
2026-11-08. Confirmed against the Terraform variables and outputs pages (description argument, prompting for variables without a default) and the terraform-docs introduction (purpose, markdown table, manual / pre-commit / CI use, .terraform-docs.yml). Removed as unconfirmed: registry, HCP no-code and terraform-ls display claims, the prompt text format, the CloudWatch retention values, tflint rule names and the terraform-docs command-line flags.
Method: documentation only; no commands were run.
