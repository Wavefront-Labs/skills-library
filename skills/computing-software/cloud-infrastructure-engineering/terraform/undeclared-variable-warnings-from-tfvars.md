---
id: computing-software.cloud-infrastructure-engineering.terraform.undeclared-variable-warnings-from-tfvars
name: undeclared-variable-warnings-from-tfvars
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, undeclared-variable, tfvars, variable-precedence, troubleshooting]
level: practitioner
status: verified
description: "Handle Value for undeclared variable warnings and errors from tfvars, -var and TF_VAR_: when it is a warning, when an error, and how to keep shared tfvars files tidy."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files", "https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undeclared variables

## Behaviour by source
| Source | Undeclared variable result |
|---|---|
| `terraform.tfvars`, `*.auto.tfvars`, `-var-file` | **Warning**: `Value for undeclared variable`; with 8 undeclared names in one file the first two were listed and the rest folded into a `Values for undeclared variables` warning |
| `-var 'x=1'` on the CLI | **Error**: `Value for undeclared variable` (`A variable named "zzz" was assigned on the command line`) |
| `TF_VAR_x` environment variable | silently ignored (`plan` showed no warning) |

```
Warning: Value for undeclared variable
The root module does not declare a variable named "enviroment" but a value was found
in file "terraform.tfvars". If you meant to use this value, add a "variable" block...
```

## Why it matters
- **Typos**: `enviroment = "prod"` in tfvars is ignored; the variable you meant falls
  back to its default (maybe `dev`). This is the dangerous case.
- **Shared tfvars** across several root modules produce warning noise that hides typos.
- Stale values after removing a variable.

## Practices
- Treat warnings as errors in CI:
```bash
terraform plan -var-file=prod.tfvars -no-color 2>&1 | tee plan.txt
grep -q "undeclared variable" plan.txt && { echo "undeclared variable in tfvars"; exit 1; }
```
- One tfvars per root module per environment; share common values with
  `*.auto.tfvars` symlinks rather than one giant file.
- Remove required defaults for environment-critical variables (`environment`) so a
  typo fails as `No value for required variable`.
- (The singular and plural titles both contain `undeclared variable`, so one grep matches either.)
- TF_VAR_ typos are invisible; prefer tfvars for important values or validate with
  a precondition.

## Verify
- [ ] CI fails on undeclared variable warnings.
- [ ] Critical variables have no default.

## Checked
- Terraform 1.17.0 in a scratch module: undeclared names in `terraform.tfvars`, a `.auto.tfvars` file (8 names, first two shown then a plural summary) and `-var-file` gave warnings; `-var` gave an error on `plan`, `apply` and `console`; `TF_VAR_` gave nothing; a typo'd tfvars name left the variable at its default.
- Removed the unchecked HCP Terraform workspace-variable row.
