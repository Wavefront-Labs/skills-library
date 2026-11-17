---
id: computing-software.cloud-infrastructure-engineering.terraform.running-module-tests-in-the-hcp-private-registry
name: running-module-tests-in-the-hcp-private-registry
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, registry-tests, terraform-test, private-registry, hcp-terraform, module-testing]
level: practitioner
status: docs-checked
description: "Run terraform test for private registry modules in HCP Terraform: enabling tests, test environment variables and dynamic credentials, terraform test -cloud-run, and cleanup."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/registry/test", "https://developer.hashicorp.com/terraform/cli/commands/test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module tests in the HCP private registry

## Enable
Testing needs a module that uses the **branch-based publishing** workflow and whose source includes tests. HCP Terraform then runs the tests for every commit to the designated branch, to help you verify it is safe to publish new module versions.
- New module: choose the Branch module publishing type, assign a branch and a module version, tick **Enable testing for module**, then **Publish module**.
- Existing module: on the module overview screen click **Configure Tests**, then **Enable testing for module**.

## Environment variables and credentials
- On the module overview screen click **Configure Tests**; in the Variables section click **+ Add variable**, give a Key and Value and tick **Sensitive** to protect the value. Unconfigured string-typed `TF_VAR_x` variables must be wrapped in double quotes.
- If tests provision infrastructure you must configure provider credentials for the module.
- Preferred: dynamic credentials via OIDC, which generate a unique short-lived token for each test run instead of static environment variables. The page says this is available in the Standard, Plus and Enterprise tiers; the setup steps are on its "Use dynamic credentials with module testing" page, not read for this skill.
- Test-specific provider configuration is covered by the Terraform test docs.

## Run remotely from your machine
After publishing with testing enabled, trigger a remotely executed test run without committing to version control, using the credentials configured in HCP Terraform:
```bash
terraform login
terraform test -cloud-run=app.terraform.io/:ORG/:MODULE_NAME/:PROVIDER
```
- `-cloud-run` takes a **private registry** module source (not the public registry) and associates the run with that module in the HCP Terraform UI.
- Run `terraform login` first, and make sure the hostname matches the private registry hostname of the module.
- `-junit-xml` is currently incompatible with `-cloud-run`.

## What runs
Standard `terraform test`: it looks for `.tftest.hcl` files in the main configuration directory and in `tests/` (the default test directory). Tests that apply create real infrastructure. Terraform attempts to destroy what remains after each test file and reports resources it could not destroy; the docs recommend dedicated test accounts that you can routinely purge.

## Generated tests
HCP Terraform can generate test files for a private module (public beta; **Generate tests** on the module overview, one time per module): download them and unzip into a `tests` directory in your configuration.

## Checked
Date: 2026-11-07. Read in full: "Test private modules in the HCP Terraform private registry" and the `terraform test` command page (options, state management, cleanup, HCP Terraform execution). Removed because neither page states them: the `TFC_AWS_PROVIDER_AUTH` / `TFC_AWS_RUN_ROLE_ARN` variable names, the agent pool option, tests running on pull requests, "require passing tests before a version is published", the output-streams-back wording, the Gotchas (runner tooling, concurrency counting, registry variables separate from workspace variable sets) and the Verify list. The `-cloud-run` argument is now shown with the page's `:ORG/:MODULE_NAME/:PROVIDER` placeholders instead of an invented module address.
Method: documentation only; no commands were run.
