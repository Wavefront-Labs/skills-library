---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-test-run-blocks-and-expect-failures
name: terraform-test-run-blocks-and-expect-failures
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-test, run-block, command-plan, expect-failures, assert, tftest-hcl]
level: practitioner
status: verified
description: "Write .tftest.hcl files: run blocks with command = plan or apply, assertions, per-run variables, referencing earlier runs, and negative tests with expect_failures."
sources: ["https://developer.hashicorp.com/terraform/language/tests", "https://developer.hashicorp.com/terraform/cli/commands/test", "https://opentofu.org/docs/cli/commands/test/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform test`: run blocks and `expect_failures`

## Layout
```
modules/bucket/
  main.tf variables.tf outputs.tf
  tests/
    defaults.tftest.hcl
    validation.tftest.hcl
```
`terraform test` (1.6+, v1.6 changelog) discovers `*.tftest.hcl` in the root dir and
`tests/` (both ran). Text below uses a module with a `local_file` resource; the
examples ran under Terraform 1.17.0.

## Run blocks
```hcl
# tests/defaults.tftest.hcl
variables {                          # file-level defaults for all runs
  name = "unit-test-bucket"
}

run "plan_defaults" {
  command = plan                     # no real infrastructure
  assert {
    condition     = local_file.f.content == "hello unit-test cfgv"
    error_message = "Content should come from var.name and the data source."
  }
}

run "apply_and_check_output" {
  command = apply                    # default; creates real resources, destroyed at end of the file
  variables {
    name = "it-${run.plan_defaults.name}"   # values from earlier runs: run.<name>.<output>
  }
  assert {
    condition     = output.file_id != ""
    error_message = "file_id output must be set."
  }
}
```
- `command = plan`: fast unit tests; attributes unknown until apply cannot be asserted
  (`local_file.f.id == ""` failed with `Unknown condition value`).
- Runs execute in order and share state within the file.
- Assertions can reference resources, data sources, outputs, variables, locals of the module.

## Negative tests
```hcl
run "rejects_bad_name" {
  command = plan
  variables { name = "Bad_Name" }
  expect_failures = [var.name]       # the validation on var.name must fail
}
```
`expect_failures` accepts variables, outputs, resources/data (pre/postconditions)
and `check` blocks (all four ran). The run passes only if exactly those fail:
listing `var.m` when `var.m` was valid failed with `Missing expected failure`, and
a second invalid variable that was not listed failed the run with
`Invalid value for variable`. Use `command = plan` when expecting a resource
postcondition or output precondition: with `command = apply` the run fails (the
expected failure stops the apply, reported as `Expected failure while planning`).
A failed run makes the rest of the file's runs `skip`.

## Running
```bash
terraform init
terraform test
terraform test -verbose          # show plan/state per run
```

## Gotchas
- `command = apply` costs money and time — keep most tests `plan`.
- A run whose apply fails (a failing `local-exec` provisioner) still shows
  `tearing down` before the file result; see the cleanup skill for leftovers.
- A `provider "local" {}` block in the test file was accepted; use such blocks for
  test-specific provider configuration.
- On Windows, `-filter` takes the native path (`tests\defaults.tftest.hcl`); with `/`
  it silently ran 0 tests.

## Verify
- [ ] `terraform test` reports `N passed, 0 failed`.
- [ ] Breaking the validation rule makes `rejects_bad_name` fail.

## Checked
- Terraform 1.17.0 with `hashicorp/local`: ran the defaults/apply/negative layout (plan assert, `run.<name>.<output>` variable, file-level `variables`), root-dir and `tests/` discovery, `expect_failures` with variables, an output precondition, a resource postcondition and a `check` block (plan vs apply behaviour, missing and unlisted failures), `-verbose`, a failed provisioner apply, and a `provider` block in a test file.
- v1.6 changelog for the `terraform test` introduction. The S3 bucket examples were replaced by `local` equivalents; no cloud resource was applied.
