---
id: computing-software.cloud-infrastructure-engineering.terraform.validate-with-test-files-and-no-tests
name: validate-with-test-files-and-no-tests
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, validate-no-tests, terraform-validate, terraform-test, tftest-hcl]
level: practitioner
status: verified
description: "Understand how terraform validate checks .tftest.hcl files, use -no-tests and -test-directory, and fix test-file validation errors before terraform test runs."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/validate", "https://developer.hashicorp.com/terraform/language/tests", "https://developer.hashicorp.com/terraform/cli/commands/test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `validate` and test files
`terraform validate` also validates `.tftest.hcl` files found in the current directory
and the test directory (default `tests/`); Terraform 1.9.8 and 1.17.0 both did (each
rejected a bogus argument in a test file).
```bash
terraform validate                          # config + test files
terraform validate -no-tests                # config only
terraform validate -test-directory=testing  # non-default test dir
```
All three flags are in `terraform validate -help` (1.9.8 and 1.17.0), and the
`-test-directory` run reported a broken file in `testing/` while plain `validate` ignored it.

## What it catches in tests (ran)
- Syntax errors and unknown arguments or blocks in test files (`Unsupported argument`,
  `Unsupported block type`, reported against `tests\file.tftest.hcl`).
- `module { source = ... }` in a run block pointing at a path that is not installed
  (`Module not installed`).

## What it does NOT catch (ran, `valid: true`)
- An `assert` condition referencing a resource that does not exist (`local_file.nope.id`)
  or an output that does not exist (`output.nope`).
- `expect_failures = [var.nope]` pointing at an undeclared variable.
`terraform test` caught the first (`Reference to undeclared resource`, remaining runs
skipped); those mistakes need a test run, not `validate`.

## Why use `-no-tests`
- Tests reference helper modules under `tests/setup`; with those not installed
  (no `terraform init` yet) plain validate reports `Module not installed`, while
  `-no-tests` validates only the main configuration.
- A lightweight CI job validating the module does not need the test files at all.

## Typical CI split
```bash
terraform init -backend=false
terraform validate -no-tests     # fast gate
terraform test -verbose          # full test job, also validates tests
```

## Gotchas
- A test-only syntax error fails plain `validate`; the message points at the
  `.tftest.hcl` file, not your `.tf`.
- Validate does not evaluate assertions; only `terraform test` runs them (a failing
  `assert` was not reported by validate).
- With a non-default test directory, give the same `-test-directory` to `init`,
  `validate` and `test`.

## Verify
- [ ] `terraform validate` passes with tests included in at least one CI job.
- [ ] Test directory flag matches between validate and test commands.

## Checked
- Terraform 1.17.0 (and 1.9.8 for the version gate) in scratch modules with `hashicorp/local`: validated test files containing a bogus argument, an unknown block, a missing helper module path, an assert on a missing resource and output, and `expect_failures` on an undeclared variable (JSON `valid` and diagnostics read with jq); ran `-no-tests` and `-test-directory`; ran `terraform test` on the missing-resource assert.
- Removed unrun claims about OpenTofu `.tofutest.hcl` and the "older Terraform" CI split. The 1.6 gate was dropped (the 1.6 changelog does not mention validate).
