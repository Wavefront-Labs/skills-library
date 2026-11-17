---
id: computing-software.cloud-infrastructure-engineering.terraform.interactive-variable-prompts-and-input-false
name: interactive-variable-prompts-and-input-false
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, variable-prompt, input-false, tf-input, non-interactive, variables]
level: practitioner
status: verified
description: "Understand when Terraform prompts for variable values, why CI hangs or fails with No value for required variable, and how -input=false, TF_INPUT and defaults change it."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#assigning-values-to-root-module-variables", "https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_input", "https://developer.hashicorp.com/terraform/cli/commands/plan#input-false"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable prompts and `-input=false`

## When Terraform prompts
A **root module** variable without a default and without a value from tfvars, `-var`,
or `TF_VAR_` triggers an interactive prompt during plan/apply (`terraform console` with piped stdin did not prompt; it printed `(known after apply)`):
```
var.db_password
  Master password for the database.
  Enter a value:
```
The description is shown (run). Echo suppression for `sensitive` variables needs a terminal and was not checked.

## In automation
| Setting | Behaviour on missing required variable |
|---|---|
| default (input enabled) | prompts on stdin; with stdin closed (`< /dev/null`) both prompts printed and it then failed `No value for required variable` (a CI step that keeps stdin open would wait) |
| `-input=false` | fails immediately: `Error: No value for required variable` |
| `TF_INPUT=0` (or `false`) | same as `-input=false` for all commands |
| `TF_IN_AUTOMATION=1` | does **not** disable prompts (the prompts still printed) |

Always run CI with `-input=false` (or `TF_INPUT=0`); `TF_INPUT=false` also worked.

## Fixes for the error
- Provide the value: tfvars file, `-var`, `TF_VAR_name`.
- Give a default if the variable is genuinely optional.
- Prompts only exist for root-module variables (see above); a missing required child-module argument is a configuration error.

## Empty strings
Pressing enter at a prompt sets `""` (run: validation reported `var.plain is ""`);
validation should catch empty strings for required inputs:
```hcl
validation {
  condition     = length(trimspace(var.db_password)) > 0
  error_message = "db_password must not be empty."
}
```

## Verify
- [ ] CI plans use `-input=false` or `TF_INPUT=0` and fail fast on missing values.

## Checked
- Terraform 1.17.0 with a required `sensitive` variable: default prompts with closed stdin (`< /dev/null`), piped empty and non-empty answers, `-input=false`, `TF_INPUT=0` and `TF_INPUT=false`, `TF_IN_AUTOMATION=1`, and a validation block on an empty answer.
- Corrections: closed stdin does not hang, it errors after printing the prompts; `TF_IN_AUTOMATION` leaves prompts enabled (kept). Removed unrun claims about `init` prompts and sensitive echo suppression (needs a TTY).
