---
id: computing-software.cloud-infrastructure-engineering.terraform.hcl-style-conventions-beyond-fmt
name: hcl-style-conventions-beyond-fmt
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hcl-style, style-conventions, terraform-fmt, code-style, tflint]
level: practitioner
status: docs-checked
description: "Know that terraform fmt applies only a subset of the documented Terraform style conventions, and cover the rest with the TFLint terraform ruleset and code review."
sources: ["https://developer.hashicorp.com/terraform/language/style", "https://developer.hashicorp.com/terraform/cli/commands/fmt", "https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/rules/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCL style: fmt vs the style guide

## What `fmt` does
- Applies "a subset of the Terraform language style conventions, along with other minor adjustments for readability".
  It has no customisation options; the canonical format may change in minor ways between Terraform versions, so run it
  after an upgrade.
- Documented conventions it is meant to apply: two-space indentation per nesting level and aligned `=` signs for
  consecutive single-line arguments.
- Flags: `-check` (non-zero exit and a list of unformatted files), `-diff`, `-recursive` (default is current
  directory only), `-list=false`, `-write=false`, `-no-color`. Targets: a directory, a file, or `-` for stdin.
- The docs recommend following the documented style even where `fmt` does not apply it automatically.

## Style guide rules and how to cover them
`fmt` is not documented as applying these, so treat them as review items unless a linter rule exists.

| Guide rule | Cover with |
|---|---|
| Within a block: meta-arguments (`count`/`for_each`) first, a blank line, then arguments, a blank line, then nested blocks; `lifecycle` and `depends_on` last | review |
| Blank lines between top-level blocks and between logical groups of arguments | review |
| Resource names: descriptive noun, underscores between words, no resource type in the name, quote type and name | `terraform_naming_convention` (TFLint) |
| `type` and `description` on every variable; `description` on every output | `terraform_typed_variables`, `terraform_documented_variables`, `terraform_documented_outputs` |
| Variable parameter order: type, description, default, sensitive, validation | review |
| No unused variables, data sources, locals | `terraform_unused_declarations` |
| Pin versions: providers via `required_providers`, Terraform via `required_version`, registry modules via `version` | `terraform_required_providers`, `terraform_required_version`, `terraform_module_version` |
| Git or Mercurial module sources pinned | `terraform_module_pinned_source` |
| `#` for single and multi-line comments, not `//` or `/* */` | `terraform_comment_syntax` |
| Standard module structure | `terraform_standard_module_structure` |
| Use `count` and `for_each` sparingly; `count` for near-identical resources, `for_each` when arguments need distinct values | review |
| Define data sources before the resources that reference them | review |
| Always include a default (alias-less) provider configuration, defined first | review |
| 0.11-style interpolation | `terraform_deprecated_interpolation` |

## File names the style guide recommends
`backend.tf`, `main.tf`, `outputs.tf` (outputs alphabetical), `providers.tf`, `terraform.tf` (one `terraform` block
with `required_version` and `required_providers`), `variables.tf` (alphabetical), `locals.tf`, `override.tf`. Split
large configurations by logical group (for example `network.tf`, `storage.tf`, `compute.tf`).

## TFLint
The TFLint terraform ruleset implements recommendations from the Terraform language documentation and has no
configurable style rules. All rules are enabled by default; `preset = "recommended"` enables only the rules marked
Recommended in the rules list. Several rules above (`terraform_naming_convention`,
`terraform_standard_module_structure`, `terraform_documented_*`, `terraform_comment_syntax`) are not in the
Recommended set, so enable them deliberately. See the TFLint configuration docs for the config syntax.

## Verify
- [ ] `terraform fmt -check -recursive` passes in CI.
- [ ] TFLint runs in CI with the rules you chose.
- [ ] Review checklist covers meta-argument ordering and naming.

## Checked
Confirmed 2026-11-08 against the Terraform Style Guide, the `terraform fmt` page and the TFLint terraform ruleset
rules list: fmt flags, the style rules and file names, the rule names and which are marked Recommended. Removed: claims
about which file types fmt formats, legacy-syntax rewriting, trailing-whitespace handling, TFLint `preset = "all"`,
`rule` block syntax and the `tflint --recursive` command (not on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
