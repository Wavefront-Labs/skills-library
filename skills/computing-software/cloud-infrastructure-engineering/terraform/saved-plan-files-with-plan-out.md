---
id: computing-software.cloud-infrastructure-engineering.terraform.saved-plan-files-with-plan-out
name: saved-plan-files-with-plan-out
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plan-out, saved-plan-file, binary-plan, terraform-plan, terraform-apply, plan-artifact, terraform-show, stale-plan]
level: practitioner
status: verified
description: "Write a plan with -out, inspect it with show, and apply exactly that plan: what a binary plan contains, why it goes stale, and how to ship it between CI stages safely."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#out-filename", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/cli/commands/show", "https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saved plan files with `plan -out`

**Goal:** guarantee that what a reviewer approved is exactly what gets applied — no
re-planning between approval and apply.

## 1. Write, inspect, apply
```bash
terraform plan -out=tfplan            # binary file, not text
terraform show tfplan                 # human-readable rendering
terraform show -json tfplan > plan.json
terraform apply tfplan                # no prompt, no re-plan; -auto-approve is implied
```
- `apply <planfile>` does not take new inputs: `apply -var n=b tfplan` failed with the
  confusing `Value for undeclared variable` error (the variable was not applied), and
  `-target` printed `Warning: Can't change resource targeting when applying a saved
  plan` ("This flag will be ignored") and still applied the plan. Variables and targets
  are baked in at plan time.
- The file is a zip archive (Python `zipfile` lists `tfplan`, `tfstate`, `tfstate-prev`,
  `tfconfig/m-/main.tf`, `tfconfig/modules.json`, `.terraform.lock.hcl`). A sensitive
  variable's value (`S3CRET-VALUE-123`) was found in plaintext in the `tfplan` entry and the
  config copy. Treat the file as a secret artefact; delete after apply.
- `terraform show -json tfplan` has `format_version` `1.2` here, with
  `resource_changes[].change.after` and `after_sensitive` (`{"input":true}`).
- `terraform show tfplan` worked in a directory with no `init` when the plan only used the
  built-in provider; whether plans with other providers need plugins to render was not tested.
## 2. Stale plans
Apply compares the state with the snapshot in the plan. After applying plan B, applying
the earlier plan A failed with `Error: Saved plan is stale` ("The given plan file can no
longer be applied because the state was changed by another operation after the plan was
created"); a second `apply` of the same file fails the same way. This is the feature: an
approved plan can never clobber a newer apply.
A plan is also rejected when the Terraform version differs: `plan file was created by
Terraform 1.17.0, but this is 1.9.8; plan files cannot be transferred between different
Terraform versions` (`terraform show` gives the same reason).
Things that did NOT block the apply in 1.17.0: appending a comment line to `main.tf` and
appending a comment to `.terraform.lock.hcl` after planning (the plan carries its own copy).
## 3. Shipping between CI stages
```bash
terraform plan -input=false -out=tfplan        # plan job: upload tfplan as a short-lived artefact
terraform show -no-color tfplan                # render for the PR comment
# apply job, after the approval gate, with the same Terraform version and commit
terraform init -input=false && terraform apply -input=false tfplan
```
- Pin the Terraform version in both jobs (the plan file is version specific).
- Check out the **same commit** in the apply job; a changed `.tf` file may not block the
  apply (see above), so the guard is your pipeline, not Terraform.
- Short retention; the artefact contains secrets.
- Render `terraform show -no-color tfplan` into the PR comment so reviewers see the
  text of the same file that will be applied.
## 4. Empty plans and exit codes
`plan -out` wrote the file even with no changes (and `apply` of it reported 0 changes).
Combine with `-detailed-exitcode` (ran: 0 = no changes, 1 = error, 2 = changes) to skip
the apply stage when nothing changed.

## Gotchas
- `-out` plus `-destroy` produces a destroy plan; `apply` of that file destroyed with
  no prompt (`Apply complete! Resources: 0 added, 0 changed, 1 destroyed`). Name it `destroy.tfplan` so nobody applies it by accident.
- `terraform show -json` output for a saved plan includes `configuration`; the sensitive
  mask is `resource_changes[].change.after_sensitive`, but the unmasked `after` value is
  also in the JSON.
- The plan format is not a documented interface (zip of internal entries); parse
  `terraform show -json` instead.

## Verify
- [ ] `terraform apply tfplan` runs without a prompt and prints the same change counts as the earlier plan.
- [ ] Applying a second time fails with "Saved plan is stale".
- [ ] CI artefact retention is short and the apply job checks out the same commit and Terraform version.

## Checked
- Terraform 1.17.0 (and 1.9.8 for the version mismatch) with a `terraform_data` resource and a sensitive variable: `plan -out`, `show`, `show -json`, `apply tfplan` (no prompt), `apply -var`/`-target` against a saved plan, zip entries and plaintext secret check with Python, stale plan after another apply, second apply, version mismatch error text, config and lock-file edits after planning, no-change `-detailed-exitcode` 0/2/1, and a destroy plan.
- Corrections: the file is a zip (not gzip+JSON); changing `main.tf` or the lock file after planning did not block the apply; `apply -var` fails with an undeclared-variable error and `-target` is only a warning; `show` worked without init for a built-in-provider plan. Removed the unchecked GitHub Actions YAML and the HCP Terraform claim.
