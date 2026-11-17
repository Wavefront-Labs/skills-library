---
id: computing-software.cloud-infrastructure-engineering.terraform.tflint-config-and-rulesets
name: tflint-config-and-rulesets
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tflint, tflint-config, tflint-ruleset, linting, static-analysis, ci]
level: practitioner
status: docs-checked
description: "Configure TFLint with .tflint.hcl: the terraform preset, cloud rulesets (aws/azurerm/google), module inspection, ignores and CI usage."
sources: ["https://github.com/terraform-linters/tflint/blob/master/docs/user-guide/config.md", "https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/rules/README.md", "https://github.com/terraform-linters/tflint-ruleset-aws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TFLint configuration and rulesets

## .tflint.hcl
```hcl
config {
  call_module_type = "local"        # all | local (default) | none; "all" also inspects remote modules
}

plugin "terraform" {
  enabled = true
  preset  = "recommended"           # only the rules marked Recommended; omit to enable every rule
}

plugin "aws" {
  enabled = true
  version = "<version>"             # pin an exact release of the ruleset
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}
rule "terraform_documented_variables" { enabled = true }
```
The `terraform` ruleset ships bundled with TFLint; declare a `plugin "terraform"` block with `version` and `source` only if you want a different release (the bundled one is then not enabled automatically).

## Running
```bash
tflint --init                          # downloads plugins declared in .tflint.hcl
tflint --recursive --format=sarif --call-module-type=local   # every directory with .tf files
tflint --chdir=live/prod/network --var-file=prod.tfvars
```
- `--format` values: default, json, checkstyle, junit, compact, sarif.
- Exit status: 0 no issues, 1 errors occurred, 2 issues found and no errors; `--force` returns 0 even when issues are found.
- In `--recursive` mode the config-file fields `format`, `call_module_type` and `force` are ignored; pass them as flags.
- `tflint --init` calls the GitHub API, which is rate-limited when unauthenticated; set `GITHUB_TOKEN` (in GitHub Actions pass the built-in token) to raise the limit.

## What it catches that validate doesn't
- Provider-specific errors that are valid HCL, for example an invalid EC2 instance type, via the cloud rulesets. The AWS ruleset lists 700+ rules and not all are enabled by default; best-practice rules need enabling.
- `terraform_unused_declarations` (unused variables, data sources, locals), `terraform_deprecated_index`, `terraform_required_providers` (version constraints), `terraform_documented_variables`, `terraform_naming_convention`, `terraform_standard_module_structure`.

## Ignoring
```hcl
# tflint-ignore: terraform_naming_convention
variable "legacyName" {}
```
`# tflint-ignore-file: rule_name` suppresses a rule for a whole file. Set `ignorable = false` in a rule block to stop annotations suppressing that rule. Add a comment saying why.

## Gotchas
- Plugins are pinned by `version`; bump them like providers.
- With `--chdir` or `--recursive`, a relative `--config` path is resolved against each module directory, so a single root config can be missed; pass an absolute path: `--config "$(pwd)/.tflint.hcl"`.

## Verify
- [ ] `tflint --init` then `tflint --recursive --config "$(pwd)/.tflint.hcl"` exits 0 in CI.
- [ ] A deliberately invalid instance type in a test branch fails the lint job.

## Checked
2026-10-28. Confirmed against the TFLint config guide, the plugins guide, the tflint-ruleset-terraform rules README and the tflint-ruleset-aws README: `call_module_type` values, `format` values, exit statuses, `--force`, recursive-mode flag-only fields, absolute `--config` path, `GITHUB_TOKEN` for `--init`, `preset = "recommended"`, bundled terraform plugin, rule names, `tflint-ignore` and `tflint-ignore-file` annotations, `ignorable`, 700+ AWS rules.
Removed or corrected: `format` and `call_module_type` in the config under `--recursive` (ignored there); `deep_check` and a pinned `0.37.0` plugin version (not documented); the `aws_instance_invalid_type` and `aws_instance_previous_type` rule names, `preset = "all"`, "wrong regions", and the claim that `call_module_type = "all"` needs `terraform init` (not in the fetched pages).
Method: documentation only; no commands were run.
