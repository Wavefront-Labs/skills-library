---
id: computing-software.cloud-infrastructure-engineering.terraform.fmt-and-validate-in-local-and-ci-checks
name: fmt-and-validate-in-local-and-ci-checks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-fmt, terraform-validate, fmt, validate, pre-commit, ci, linting, tflint, formatting, static-checks]
level: intro
status: docs-checked
description: "Run terraform fmt and terraform validate correctly in pre-commit and CI: the right flags, the init -backend=false trick, and what validate cannot catch."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/fmt", "https://developer.hashicorp.com/terraform/cli/commands/validate", "https://github.com/antonbabenko/pre-commit-terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# terraform fmt and validate in local and CI checks

**Goal:** make formatting and syntax/type errors impossible to merge, with checks that
run in seconds and need no cloud credentials.

## 1. `terraform fmt`
```bash
terraform fmt                 # rewrite files in the current dir
terraform fmt -recursive      # include subdirectories (modules/)
terraform fmt -check -diff    # CI mode: non-zero exit if anything would change, show the diff
terraform fmt -list=false -write=false -diff   # same, quieter
```
- `-check` exits 0 when the input is formatted, otherwise non-zero, and lists the
  improperly formatted files; it implies `-write=false`, as does reading from stdin.
- `fmt` scans the current directory by default; a target can be a directory, a file or
  `-` (stdin). Subdirectories need `-recursive`.
- It has no customisation options by design. Its canonical format may change in minor
  ways between Terraform versions, so run it on your modules after upgrading.
- OpenTofu: `tofu fmt`.

## 2. `terraform validate`
```bash
terraform init -backend=false   # initialise without accessing the configured backend
terraform validate
terraform validate -json        # machine-readable output; always disables colour
```
- Validation needs an initialised directory with referenced plugins and modules
  installed, so `init -backend=false` still needs network access (or a provider mirror)
  but no backend credentials.
- It checks that a configuration is syntactically valid and internally consistent,
  including attribute names and value types, regardless of variables or existing state.
  It does not validate remote services such as remote state or provider APIs.
- To check a configuration in the context of a particular run (workspace, variable
  values), use `terraform plan`, which includes an implied validation check.
- `-json` output has `valid`, `error_count`, `warning_count` and `diagnostics`; consumers
  should expect non-JSON text on stdout if Terraform fails before validation starts.
- `-var` / `-var-file` are accepted if a root-module check needs values.
- It is safe to run automatically, for example on save or as a CI step for a module.

## 3. Pre-commit hooks
The `pre-commit-terraform` project provides `terraform_fmt`, `terraform_validate`,
`terraform_tflint` and `terraform_docs` hooks:
```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: <VERSION>   # latest from the project's releases page
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
```
`terraform_tflint` needs TFLint installed, `terraform_docs` needs terraform-docs
0.12.0 or newer, and `terraform_validate` with `--retry-once-with-cleanup` needs `jq`.

## 4. CI job
Run on every PR before the plan job:
```bash
terraform fmt -check -recursive -diff
terraform init -backend=false -input=false
terraform validate -no-color
```
Pin the Terraform version your CI uses, because the canonical format can change
between versions.

## 5. Beyond validate
- TFLint is a separate linter for provider-specific rules; keep it alongside validate.
- `terraform plan` is the check that uses real state and variable values; keep
  fmt/validate as the fast gate, not the only gate.

## Gotchas
- `validate` on a root module with a remote backend block, without `-backend=false`
  at init, tries to reach the backend and fails in CI without credentials.

## Verify
- [ ] `terraform fmt -check -recursive` exits 0 on main.
- [ ] `terraform init -backend=false` then `terraform validate` runs green in CI without cloud credentials.

## Checked
2026-10-31. Confirmed against the Terraform `fmt` and `validate` command pages (flags,
`-check` semantics, targets, no customisation, `init -backend=false`, JSON fields,
remote services not validated, `plan` for run context) and the pre-commit-terraform
README (hook ids, TFLint, terraform-docs 0.12.0+, `jq` for the retry flag). Removed:
exit code 3, fmt "never changes semantics", `.tf.json` and heredoc behaviour,
the list of specific errors validate catches, the pinned hook revision and Terraform
version, the `hashicorp/setup-terraform` step, what the retry flag does, and the
`${var.x}`, `0.13upgrade` and `required_providers` gotchas.
Method: documentation only; no commands were run.
