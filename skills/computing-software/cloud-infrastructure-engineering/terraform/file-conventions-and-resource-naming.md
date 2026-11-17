---
id: computing-software.cloud-infrastructure-engineering.terraform.file-conventions-and-resource-naming
name: file-conventions-and-resource-naming
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, file-conventions, versions-tf, naming-conventions, resource-naming, style-guide]
level: practitioner
status: docs-checked
description: "Apply the standard file layout (main, variables, outputs, versions, providers, locals) and naming conventions for resources, variables and cloud object names."
sources: ["https://developer.hashicorp.com/terraform/language/style", "https://developer.hashicorp.com/terraform/language/modules/develop/structure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File conventions and naming

## Files (from the Terraform style guide)
| File | Contents |
|---|---|
| `terraform.tf` | one `terraform` block with `required_version` and `required_providers` |
| `backend.tf` | backend configuration (a separate `terraform` block is allowed) |
| `providers.tf` | all provider blocks and configuration |
| `main.tf` | all resource and data source blocks; split by logical group when large (`network.tf`, `storage.tf`, `compute.tf`) |
| `variables.tf` | all `variable` blocks, alphabetical |
| `outputs.tf` | all `output` blocks, alphabetical |
| `locals.tf` | local values referenced from several files (a file-specific local goes at the top of that file) |
| `override.tf` | override definitions; Terraform loads this and `*_override.tf` last; use sparingly and comment the original resource |

Order inside a resource block: `count` or `for_each` first, then non-block arguments, then nested blocks, then `lifecycle`, then `depends_on`. Define data sources before the resources that reference them. In variables put type, description, default, sensitive, then validation; in outputs put type, description, value, then sensitive. Give every variable a type and a description and every output a description.

## Terraform names (the label)
- Use descriptive nouns with underscores between words, and do not repeat the resource type: `aws_instance.web_api`, not `aws_instance.web_api_instance`. Quote the type and name in the resource definition.
- Variable, output and local names also use descriptive nouns separated by underscores.

## Cloud object names
```hcl
locals {
  name_prefix = "${var.org}-${var.env}-${var.app}"      # acme-prod-api
}
resource "aws_s3_bucket" "logs" {
  bucket = "${local.name_prefix}-logs-${data.aws_caller_identity.current.account_id}"
}
```
- Pick one order (for example org, environment, application, purpose) and apply it everywhere.
- Check each provider's documentation for name length and character limits, and keep per-resource formatting in a naming module or locals.
- Where a service requires globally unique names, add a suffix such as an account ID or a random value.
- Changing a name can force replacement, so decide the convention before production.

## Tooling
`terraform fmt` for whitespace (add `-recursive` for subdirectories); run `terraform validate` too. A linter such as TFLint, with the `terraform_naming_convention`, `terraform_standard_module_structure` and `terraform_documented_variables` rules from its terraform ruleset, enforces naming and structure.

## Verify
- [ ] `tflint --enable-rule=terraform_naming_convention` passes.
- [ ] Every module declares `required_providers` (in `terraform.tf`).

## Checked
2026-10-28. Confirmed against the Terraform style guide (file names and contents, alphabetical variables and outputs, resource and variable and output parameter order, naming rules, fmt/validate, linting) and the TFLint terraform ruleset rules README (rule names).
Corrected: `versions.tf` as a standard name (the guide uses `terraform.tf`, plus `backend.tf`), "meta-arguments (`count`/`for_each`, `provider`)" (the guide lists only `count` or `for_each` first), "required variables first", `snake_case` lowercase wording.
Removed: `data.tf`, `iam.tf`, `moved.tf`, `imports.tf` and tfvars rows, `this`/`main` naming, units-in-names and `enable_*` / `create_*` conventions, and the S3 63 and Azure 24 character limits (not in the fetched pages).
Method: documentation only; no commands were run.
