---
id: computing-software.cloud-infrastructure-engineering.terraform.variables-in-terraform-test-files
name: variables-in-terraform-test-files
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, test-variables, terraform-test, run-block, tftest-hcl, module-testing]
level: practitioner
status: verified
description: "Supply variables to terraform test: file-level variables blocks, per-run overrides, referencing earlier run outputs, tfvars and -var precedence, and sensitive test inputs."
sources: ["https://developer.hashicorp.com/terraform/language/tests#variables", "https://developer.hashicorp.com/terraform/cli/commands/test"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables in test files
Checked under Terraform 1.17.0 with a small `hashicorp/local` module (variables `name`, `size`, `vpc_id`):
```hcl
# tests/basic.tftest.hcl
variables {                       # file-level: apply to every run block
  name = "test-name"
  size = "small"
}

run "from_file_level" {
  command = plan
  assert {
    condition     = local_file.f.content == "test-name-small-none"
    error_message = "name/size not set from file-level variables."
  }
}

run "override_name" {
  variables {                     # per-run: overrides file-level values
    name = "other"
  }
  command = plan
  assert {
    condition     = local_file.f.content == "other-small-none"
    error_message = "Override not applied."
  }
}
```
Expressions work in file-level `variables`, for example `v = upper("fn")`.

## Using outputs of earlier runs
```hcl
run "setup" {
  module { source = "./tests/setup" }        # helper module with output vpc_id
}
run "main" {
  variables {
    vpc_id = run.setup.vpc_id
  }
}
```

## Precedence (measured; highest last)
1. `TF_VAR_name` environment variable
2. `terraform.tfvars`
3. `*.auto.tfvars`
4. `-var` / `-var-file` on `terraform test` (`-var` beat the tfvars files; `-var-file` also won)
5. File-level `variables {}` (it beat `-var size=cli`)
6. Run-level `variables {}` (it beat everything above)

`terraform.tfvars` / `*.auto.tfvars` placed in the test directory were also picked up.
I did not test the relative order of module-dir versus test-dir tfvars files.

## Variables that are not declared
A file-level `variables` entry for a name the module does not declare (`bogus = "y"`)
ran without error, and an undeclared `-var region=eu` was also accepted silently.

## Secrets in tests
Do not hard-code credentials; pass via `TF_VAR_*` from CI secrets. With the module
variable marked `sensitive`, an `error_message` that interpolates it is not printed:
Terraform shows a warning `Error message refers to sensitive values`, and the condition
output shows `(sensitive value)`.

## Gotchas
- `variables` blocks accept expressions, including functions and `run.<name>.<output>`;
  referencing a resource directly (`name = local_file.f.id`) fails with
  `You can only reference run blocks and variables from within Terraform Test files`.

## Verify
- [ ] Add `error_message = "name=${var.name} size=${var.size}"` to a failing assert to see which value each run used.

## Checked
- Terraform 1.17.0 with `hashicorp/local`: ran a file-level vs run-level override test, then printed `var.name`/`var.size` from asserts under TF_VAR, `terraform.tfvars`, `a.auto.tfvars`, `-var`, `-var-file`, tests-dir tfvars and file-level variables to measure the precedence (the old list put TF_VAR and -var in one tier, but TF_VAR lost to terraform.tfvars); undeclared variables, expressions, resource references in `variables`, and a sensitive variable in `error_message` all ran.
- Removed the unrun claim about plan-run unknown outputs and about variables carrying between runs.
