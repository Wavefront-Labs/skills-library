---
id: computing-software.cloud-infrastructure-engineering.terraform.common-validate-errors-and-fixes
name: common-validate-errors-and-fixes
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, unsupported-argument, missing-required-argument, terraform-validate, diagnostics, troubleshooting]
level: practitioner
status: verified
description: "Fix the errors terraform validate reports most: Unsupported argument, Missing required argument, Unsupported block type, Reference to undeclared resource, and invalid references."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/validate", "https://developer.hashicorp.com/terraform/language/syntax/configuration", "https://developer.hashicorp.com/terraform/cli/commands/providers/schema"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common `terraform validate` errors

Validate needs `terraform init` (providers' schemas; `init -backend=false` is enough). A missing required module input is reported by `init` itself before `validate` runs (`Missing required argument`), so fix those first. Errors carry file:line; the
fixes below cover most of them.

| Error | Usual cause | Fix |
|---|---|---|
| `Unsupported argument: An argument named "x" is not expected here.` | Typo, argument removed in a provider major version, or argument belongs in a nested block | Check the resource docs for the **locked** provider version; `terraform providers schema -json` to confirm; "Did you mean" hints are reliable |
| `Missing required argument: The argument "x" is required, but no definition was found.` | New required arg after upgrade, or module input with no default | Add it; for modules check `variables.tf` |
| `Unsupported block type: Blocks of type "x" are not expected here.` | Attribute written as block (`tags { }` instead of `tags = {}`) or vice versa | Use `=` for map/object attributes; blocks for nested blocks |
| `Reference to undeclared resource` / `input variable` / `local value` | Typo or resource in another module | Reference module outputs: `module.net.vpc_id` |
| `Invalid reference: A reference to a resource type must be followed by at least one attribute access` | `aws_vpc.main` used alone | `aws_vpc.main.id` |
| `Missing resource instance key` | Resource has `count`/`for_each` | `aws_instance.web[0]`, `aws_instance.web["a"]`, or a splat |
| `Unexpected resource instance key` | Indexing a single resource | Drop the index |
| `Duplicate resource "x" configuration` | Same address in two files | Rename one; check copy-pasted files |
| `Invalid function argument` / `Call to unknown function` | Function from newer TF or provider function without `required_providers` | Check `terraform version`; add the provider |
| `Variables not allowed` | Variable used in `terraform { required_version = var.v }` (confirmed) or `module { source = var.x }` (confirmed) | Literal values (OpenTofu allows some via early evaluation) |

## Workflow
```bash
terraform init -backend=false -input=false
terraform validate -no-color
terraform validate -json | jq -r '.diagnostics[] | "\(.severity) \(.range.filename):\(.range.start.line) \(.summary)"'
```

## What validate does not catch
Values from variables (validation blocks only evaluate with real values at plan),
provider API rules (invalid instance types), permissions. Run `plan` for those.

## Verify
- [ ] `terraform validate` prints `Success! The configuration is valid.`
- [ ] Fix was checked against the provider version in the lock file, not the latest docs.
