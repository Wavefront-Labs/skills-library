---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-test-mocks-and-overrides
name: terraform-test-mocks-and-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-test, mock-provider, override-resource, override-data, mock-data, unit-testing]
level: advanced
status: verified
description: "Unit-test modules without cloud credentials using mock_provider, mock_resource/mock_data defaults, and override_resource/override_data/override_module in terraform test."
sources: ["https://developer.hashicorp.com/terraform/language/tests/mocking", "https://opentofu.org/docs/cli/commands/test/#mocks-and-overrides"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocks and overrides in `terraform test` (1.7+)

## Mock a whole provider
Checked with the `hashicorp/local` provider (any provider works the same way):
```hcl
# tests/unit.tftest.hcl
mock_provider "local" {
  mock_data "local_file" {
    defaults = { content = "MOCKED" }
  }
  mock_resource "local_file" {
    defaults = { id = "mock-id" }
  }
}
run "mocked_apply" {                       # command defaults to apply: no real file is written
  variables { name = "m1" }
  assert {
    condition     = local_file.f.content == "hello m1 MOCKED"
    error_message = "got ${local_file.f.content}"
  }
  assert {
    condition     = output.file_id == "mock-id"
    error_message = "got ${output.file_id}"
  }
}
```
- Every resource/data source of a mocked provider returns fake values: computed
  attributes not in `defaults` get generated placeholders (seen: random 8-character
  strings such as `r6rxcm2f` for `id`, `content_sha256`, `file_permission`).
- No credentials needed for the mocked provider (the provider is still downloaded by `init`).
- Aliased: `mock_provider "local" { alias = "dr" }` and pass it with
  `providers = { local = local.dr }` in a run (ran).

## Override specific objects
```hcl
override_data {
  target = data.local_file.cfg
  values = { content = "OVR" }
}
override_resource {
  target = local_file.f
  values = { id = "ovr-res" }
}
override_module {
  target  = module.network
  outputs = { ids = ["subnet-a", "subnet-b"] }
}
run "uses_override" {
  override_data {                          # run-level: only this run
    target = data.local_file.cfg
    values = { content = "OVR2" }
  }
}
```
File-level overrides apply to all runs; run-level ones only to that run. All three
forms ran. Overrides also work with the real provider (no `mock_provider`): in 1.17 a
plain `command = plan` run saw the overridden data value. Terraform 1.11 added
`override_during = plan` to make overridden/mocked values visible in plan runs
(changelog v1.11).

## Shared mock data files
`mock_provider "local" { source = "./tests/mocks" }` loads `*.tfmock.hcl` files with
`mock_resource`/`mock_data` blocks (ran with a `local.tfmock.hcl`), reusable across
test files.

## Limits
- Mocks can't validate provider-side rules (for example a cloud API rejecting an
  invalid value) — keep a few real `apply` integration tests.
- Generated placeholder values are random strings and can fail your own validation
  regexes (for example an ARN format) — set realistic `defaults`.
- On Windows, `-filter` needs the native separator: `-filter=tests\unit.tftest.hcl`;
  `-filter=tests/unit.tftest.hcl` ran 0 tests with only an `Unknown test file` warning.

## Verify
- [ ] `terraform test -filter=tests\unit.tftest.hcl` (Windows; `/` elsewhere) passes with no cloud credentials in the environment.
- [ ] Changing the naming logic breaks the unit test.

## Checked
- Terraform 1.17.0, `hashicorp/local` module with a data source, resource and local child module: ran `mock_provider` with `mock_data`/`mock_resource` defaults, `source = "./tests/mocks"` with a `.tfmock.hcl`, aliased mock provider passed via `providers`, file-level `override_resource`/`override_module`/`override_data`, run-level `override_data`, overrides with the real provider, and placeholder values (random 8-char strings).
- `-filter` with a forward slash on Windows ran 0 tests with an `Unknown test file` warning; backslash worked. `terraform test` also failed on a test file with an assert that is always false (`condition must refer to an object`) and validates all test files even under `-filter`.
- Changelogs: v1.7 (mock_provider, overrides), v1.11 (`override_during`). AWS-specific mock examples were replaced by `local` equivalents, so no cloud provider was run.
