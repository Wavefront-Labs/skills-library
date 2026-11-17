---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-destroy-flags-and-plan-destroy
name: terraform-destroy-flags-and-plan-destroy
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, destroy-flags, destroy-auto-approve, destroy, plan-destroy, saved-plan-file]
level: practitioner
status: docs-checked
description: "Use terraform destroy and plan -destroy correctly: the apply -destroy alias, speculative destroy plans, saved plan files, and -target for partial destroys."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/destroy", "https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform destroy` and `plan -destroy`

## Equivalence
```bash
terraform destroy                      # alias for: terraform apply -destroy
terraform plan -destroy                # speculative destroy plan; nothing is executed
terraform plan -destroy -out=FILENAME  # save the plan, then:
terraform apply FILENAME
```
- `destroy` accepts most `apply` options, but takes no plan file argument and forces
  destroy planning mode.
- `apply -destroy` exists only in Terraform v0.15.2 and later; earlier versions need
  `terraform destroy`. In v0.15 and earlier `-destroy` was supported only by `plan`.
- Destroy mode creates a plan to destroy all remote objects that currently exist,
  leaving an empty Terraform state. It suits transient development environments; the
  destroy page notes you typically will not want to destroy long-lived production objects.
- `plan -out=FILENAME` writes an opaque plan file to pass to `apply`; without `-out`, a
  plan is speculative. The saved-plan workflow is primarily intended for automation.
- `-input=false` disables prompting for unset root module variables and is useful in
  automation; `-json` implies it.

## Partial destroy
```bash
terraform destroy -target aws_instance.example
```
`-target` destroys the named resource and its dependencies.

## Checked
Date: 2026-11-07
Read in full: `terraform destroy` command page. The plan page: read the planning modes section and the `-out`, `-input` and `-json` option text, not the whole page.
Confirmed: everything above.
Removed (not on the pages): the list of options destroy accepts, the recommendation table (CI, unattended, PR environments, `-lock-timeout` values), production guardrails (`prevent_destroy`, provider deletion protection, HCP Terraform "Allow destroy plans", policy checks), the "what destroy does not do" section (state rm, `force_destroy`, serial bump, workspace deletion), and the Verify steps with `wc`. `-auto-approve` is not described on these pages, so it is not covered here.
Method: documentation only; no commands were run.
