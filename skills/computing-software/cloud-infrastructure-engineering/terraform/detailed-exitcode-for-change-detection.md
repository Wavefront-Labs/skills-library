---
id: computing-software.cloud-infrastructure-engineering.terraform.detailed-exitcode-for-change-detection
name: detailed-exitcode-for-change-detection
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, detailed-exitcode, exit-code-2, terraform-plan, drift-check, ci-gating, no-changes, pipeline-skip, exit-codes]
level: intro
status: verified
description: "Use plan -detailed-exitcode (0 none, 1 error, 2 changes) to skip apply stages, gate drift alerts and avoid the shell traps that turn code 2 into a failed job."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#detailed-exitcode", "https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `-detailed-exitcode` for change detection

**Goal:** let the exit code — not log scraping — tell the pipeline whether there
is anything to apply.

## 1. The codes
```bash
terraform plan -detailed-exitcode -input=false -out=tfplan
# 0 = succeeded, no changes
# 1 = error
# 2 = succeeded, changes present
```
Without the flag, both "no changes" and "changes" exit 0. Works with `-out`,
`-refresh-only` and `-destroy` modes. `terraform apply` has no such flag.

## 2. Shell handling
`set -e` (and most CI runners) treat 2 as failure. Capture it explicitly:
```bash
set +e
terraform plan -detailed-exitcode -input=false -out=tfplan
rc=$?
set -e
case $rc in
  0) echo "no changes"; echo "changes=false" >> "$GITHUB_OUTPUT" ;;
  2) echo "changes";    echo "changes=true"  >> "$GITHUB_OUTPUT" ;;
  *) echo "plan failed"; exit $rc ;;
esac
```
GitHub Actions: add `continue-on-error: true` on the step or use the `if: steps.plan.outputs.exitcode == 2`
pattern that `hashicorp/setup-terraform` exposes. GitLab: use `allow_failure: { exit_codes: 2 }`.

## 3. Uses
- **Skip apply when nothing changed** — saves a manual approval and a lock.
- **Drift detection** — nightly `plan -detailed-exitcode -lock=false`; code 2 means
  drift or unapplied commits, alert on it.
- **Refresh-only drift** — `plan -refresh-only -detailed-exitcode`: 2 means the real
  world differs from state specifically.
- **Pre-commit guard** — refuse to merge a PR whose plan is 0 when it claims to
  change infrastructure (or vice versa).

## Gotchas
- Output changes only (`output_changes` non-empty, no resource changes) also give
  exit 2.
- Warnings do not affect the code; only errors give 1.
- Code 2 plus a saved plan file: remember the file is valid even for a no-op (code
  0) plan — you can apply either.
- With `-json`, exit codes are unchanged; parse `change_summary` for details.

## Verify
- [ ] Running the plan twice with no config change gives 0 the second time.
- [ ] Editing a tag value gives 2 and the pipeline's apply stage becomes eligible.
- [ ] A syntax error gives 1 and the pipeline fails.

## Checked
- Terraform 1.9.8 with the local provider: exit 2 for a first plan with changes, 0 with no changes, 0 without the flag even when changes exist, 1 for a configuration error; a `-out` plan with no changes still writes the file and applies; `terraform apply -detailed-exitcode` is rejected (`Failed to parse command-line flags`); `plan -destroy` gives 2; an output-only change gives 2; an unused variable and other warnings leave 0; `-refresh-only` gives 0 without drift and 2 after deleting the file; `-json` plan prints a `change_summary` message and keeps exit 2. `hashicorp/setup-terraform` documents the `exitcode` output and GitLab documents `allow_failure:exit_codes`.
