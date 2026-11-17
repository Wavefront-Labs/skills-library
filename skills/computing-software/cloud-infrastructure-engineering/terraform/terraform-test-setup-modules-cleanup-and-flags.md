---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-test-setup-modules-cleanup-and-flags
name: terraform-test-setup-modules-cleanup-and-flags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-test, test-helper-module, setup-module, test-cleanup, test-filter, test-junit, ci]
level: advanced
status: verified
description: "Use helper/setup modules in terraform test runs, understand destroy order and leftover resources, and run tests in CI with -filter, -junit-xml and -var-file."
sources: ["https://developer.hashicorp.com/terraform/language/tests#modules", "https://developer.hashicorp.com/terraform/cli/commands/test", "https://developer.hashicorp.com/terraform/language/tests#state-and-cleanup"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test helper modules, cleanup and CLI flags

## Setup / helper modules
A run can execute a different module, e.g. to create prerequisites or to read results:
```hcl
run "setup_net" {
  module {
    source = "./tests/setup"          # local source (registry sources are documented too)
  }
}

run "main" {
  variables {
    vpc_id = run.setup_net.vpc_id     # outputs of the helper run
  }
}

run "verify_file" {
  command = plan
  module { source = "./tests/check" }  # helper with a data source reading what "main" wrote
  variables { path = run.main.path }
  assert {
    condition     = data.local_file.chk.content == "h1-small-none"
    error_message = "File content wrong."
  }
}
```
Each distinct module gets its own state within the test file (the helper's output
`vpc_id` fed the next run; with `state_key` a run can pick another state, 1.11+).
The examples ran under Terraform 1.17.0 with `hashicorp/local`.

## Cleanup
- At the end of each test file, Terraform destroys everything it created, in
  reverse run block order (v1.7 changelog); a run whose apply failed still reached
  `tearing down`.
- Terraform 1.14 added `skip_cleanup` (test file or run block), `backend` blocks in
  run blocks and an experimental `terraform test cleanup` command; 1.16 reports the
  resources left behind when `skip_cleanup` is set (changelogs v1.14, v1.16). In
  older versions clean up leftovers manually (tag test resources and sweep). I did
  not force a failed destroy here.
- Keep helper resources cheap and in a sandbox account.

## CLI flags for CI
```bash
terraform test -filter=tests\validation.tftest.hcl     # only this file (repeatable); OS separator on Windows
terraform test -var-file=tests/ci.tfvars -var region=eu-west-1
terraform test -junit-xml=test-results.xml              # 1.11+: JUnit report for CI UIs
terraform test -test-directory=integration              # non-default dir
terraform test -parallelism=4 -verbose                  # -parallelism: 1.12+
```
All of these flags are listed by `terraform test -help` in 1.17.0 (`-junit-xml` went
GA in 1.11 and `-parallelism` arrived in 1.12 per the changelogs). `-junit-xml` wrote
`<testsuites><testsuite name=... tests="1" failures="0">` with one `testcase` per run.
On Windows `-filter=tests/x.tftest.hcl` (forward slash) ran 0 tests with only an
`Unknown test file` warning.
Split fast `plan`-only files from slow `apply` files and run them in different CI stages.

## Gotchas
- The module under test must be `init`ed (`terraform init` in the module dir), including helper module sources;
  without it the run fails with `Module not installed`. With a non-default test
  directory, pass it to init too (`terraform init -test-directory=integration`);
  plain `init` did not install helpers referenced from `integration/`.
- Helper module paths are relative to the **module under test** (`./tests/check` from
  a file in `integration/` resolved from the module root), not the test file.
- Tests share provider credentials with your shell — never run apply tests against prod credentials.

## Verify
- [ ] CI publishes the JUnit file and shows per-run results.
- [ ] After a deliberately failing test, a tag-based sweep finds zero leftovers.

## Checked
- Terraform 1.17.0 with `hashicorp/local`: ran a helper-module run whose output fed a main run, a plan-only helper with a data source reading the file written by an earlier run (assert ran), `-test-directory=integration`, init with and without `-test-directory`, `-filter` (backslash vs forward slash on Windows), `-junit-xml` (XML inspected), `-parallelism`, `-var-file`, `-verbose`, and a failed apply reaching `tearing down`.
- Changelogs v1.7 (reverse run order), v1.11 (junit GA), v1.12 (parallelism), v1.14 and v1.16 (skip_cleanup, test cleanup). HTTP helper and AWS-tag sweep examples were removed as unrun.
