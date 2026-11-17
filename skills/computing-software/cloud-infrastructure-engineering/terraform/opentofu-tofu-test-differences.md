---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-tofu-test-differences
name: opentofu-tofu-test-differences
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, tofu-test, opentofu, terraform-test, tftest-hcl, mock-providers, test-compatibility]
level: practitioner
status: docs-checked
description: "Run module tests with tofu test and know how it differs from terraform test: file extensions, mocking, provider config and migration tips."
sources:
  - https://opentofu.org/docs/cli/commands/test/
  - https://developer.hashicorp.com/terraform/language/tests
  - https://developer.hashicorp.com/terraform/language/tests/mocking
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# tofu test differences

The two test frameworks share the basics: `.tftest.hcl` files with `run` blocks, `command = plan|apply`, `assert`, `variables`, `expect_failures`, and a `module` block inside a `run` to point at another configuration (for example a setup module). They have diverged since.

## Common ground
```hcl
# tests/bucket.tftest.hcl
variables { name = "acme-test" }

run "plan_names_bucket" {
  command = plan
  assert {
    condition     = aws_s3_bucket.this.bucket == "acme-test"
    error_message = "bucket name wrong"
  }
}

run "rejects_bad_name" {
  command = plan
  variables { name = "Bad_Name" }
  expect_failures = [var.name]
}
```
- If `command` is omitted the default is a normal apply, which creates real resources. Resources are destroyed at the end, in reverse `run` block order.
- Each test file keeps its state in memory; variables set in a test file take highest precedence.
- `tofu test` accepts a flat layout (test files beside the `.tf` files) or a nested one (a `tests` directory); `-filter`, `-test-directory`, `-var`, `-var-file`, `-json` and `-verbose` are documented.

## Differences to know
| Topic | OpenTofu | Terraform |
|---|---|---|
| Test file extensions | `*.tftest.hcl`, `*.tftest.json`, `*.tofutest.hcl`, `*.tofutest.json`; when `x.tofutest.hcl` and `x.tftest.hcl` both exist only the `.tofutest` file loads | `.tftest.hcl` and `.tftest.json` |
| Minimum version | follows OpenTofu releases | test framework since v1.6.0; mocking since v1.7.0 |
| Mocking | `mock_provider` (supports `alias` and `for_each`), `mock_resource`, `mock_data`, `override_resource`, `override_data`, `override_module`; from OpenTofu 1.12 overrides can target `for_each`/`count` instances, including a wildcard key | `mock_provider` and overrides, per the Terraform mocking page |
| Provider blocks in tests | supported in test files | supported; from v1.7.0 they can reference test-file variables and run-block outputs |
| Root variables | variables used in module sources, backend config or the encryption block need values assigned when running `tofu test` | n/a on its page |
Check the docs of the exact versions you run; both add test features over time.

## Mocking example
```hcl
mock_provider "aws" {
  mock_resource "aws_s3_bucket" {
    defaults = { arn = "arn:aws:s3:::mock" }
  }
}
run "unit" {
  command = apply     # against the mock: no provider API calls
  assert {
    condition = output.bucket_arn == "arn:aws:s3:::mock"
    error_message = "arn not wired"
  }
}
```
Terraform warns that with `command = apply`, switching real providers between `run` blocks can fail because resources created by one provider definition cannot be modified by another.

## Migrating a module test suite
1. Run `tofu test` on the unchanged suite; it executes `*.tftest.hcl` files.
2. If a test needs OpenTofu-only syntax, put it in a `.tofutest.hcl` file with the same base name so the OpenTofu file wins and the `.tftest.hcl` version stays for Terraform users.
3. Run both `terraform test` and `tofu test` for modules advertised as compatible.

## Verify
- [ ] Both tools pass for modules advertised as compatible.
- [ ] Mocked unit tests run without credentials; apply-based tests clean up resources.

## Checked
2026-11-09

Method: read the OpenTofu `tofu test` docs page (raw mdx from the opentofu repository) and the Terraform tests and mocking pages (fetched as text). Removed as unsupported: the OpenTofu 1.8 mocking version claim, "tofu test doesn't touch configured backends", provider for_each and early-evaluation test features, the unverified GitHub Actions matrix, and the "tests/ or module root only" wording.
