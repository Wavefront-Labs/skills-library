---
id: computing-software.cloud-infrastructure-engineering.terraform.refresh-false-and-lock-flags-on-plan-and-apply
name: refresh-false-and-lock-flags-on-plan-and-apply
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, refresh-false, skip-refresh, lock-flag, lock-timeout, plan-speed, terraform-plan, terraform-apply, no-refresh]
level: practitioner
status: docs-checked
description: "When -refresh=false, -lock=false and -lock-timeout are the right call on plan/apply: speeding plans on big states, working around lock backends, and the drift you stop seeing."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/language/backend/s3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `-refresh=false`, `-lock` and `-lock-timeout`

**Goal:** know exactly what each of these flags trades away before you use it in
a hurry.

## 1. `-refresh=false`
By default Terraform reads the current state of existing remote objects before
comparing configuration to state. `-refresh=false` disables that synchronisation,
which can speed up planning by reducing remote API requests, but Terraform then
ignores external changes, which "could result in an incomplete or incorrect plan".
```bash
terraform plan -refresh=false -out=tfplan
```
Use it when:
- a plan takes long because of many API reads and you only changed config you fully understand;
- the provider API is rate-limited or partially down.

Do **not** rely on it for the plan you will apply in production unless a fresh plan ran
recently: drift (an attribute changed outside Terraform) is invisible.

Related options on the same page:
- `-refresh-only` is a separate planning mode that only updates state and root outputs;
  `-refresh=false` cannot be used with it.
- `-minimal-refresh` refreshes only resource instances Terraform plans to change; it also
  ignores external changes for resources with no planned changes, and cannot be combined
  with `-refresh=false` or refresh-only mode.
- Terraform refreshes a resource regardless when its schema version changes; avoid
  `-minimal-refresh` and `-refresh=false` when upgrading provider versions.

## 2. `-lock=false`
Does not hold a state lock during the operation. HashiCorp: "This is dangerous if others
might concurrently run commands against the same workspace", and it does not recommend
disabling locking. Locking is automatic on operations that could write state.
```bash
terraform plan -lock=false     # least risky: plan only previews
terraform apply -lock=false    # almost never reasonable
```
Legitimate use is narrow, for example read-only plans in parallel CI jobs when the lock
service is the bottleneck. Applying without a lock allows concurrent writers; see
`computing-software.cloud-infrastructure-engineering.terraform.state-management-and-locking`.

## 3. `-lock-timeout`
```bash
terraform apply -lock-timeout=5m
```
Unless locking is disabled, Terraform retries acquiring the lock for the given duration
(a number with a unit letter, e.g. `3s`) before returning an error. In CI with queued
jobs a few minutes of retry avoids spurious failures when the previous apply is
finishing. A lock left by a crashed run will not clear by retrying; that is
`terraform force-unlock` territory.

## 4. Combining for fast local loops
```bash
alias tfq='terraform plan -refresh=false -lock=false -compact-warnings'
```
`-compact-warnings` shows only warning summaries. Run a full `terraform plan` before
opening the PR.

## Gotchas
- A saved plan cannot take additional planning modes or options: they only affect the
  decisions that the plan file already contains. So `-refresh=false` belongs on the
  `plan` that writes the file.
- `-lock=false` on the S3 backend with `use_lockfile` means no `<key>.tflock` object
  protects the state: nothing stops a concurrent apply. (S3 locking is opt-in, with
  `use_lockfile` defaulting to false.)

## Checked
Date: 2026-11-07
Read in full: `terraform plan`, `terraform apply`, "State Locking". S3 backend page: matched lines about `use_lockfile`, `.tflock` and DynamoDB only (the page is large; read in full for another skill in this batch).
Confirmed: `-refresh=false` and `-minimal-refresh` text and restrictions, `-lock=false` warning, `-lock-timeout` text, `-compact-warnings`, saved-plan restriction, schema-version refresh note, `use_lockfile` default and `.tflock` suffix.
Removed (not on the pages): `-lock-timeout` default of `0s` for plan/apply (only documented for init), "data sources are still read", the HCP Terraform `-lock=false` rejection, the DynamoDB-throttling example, "state list/show" as lock-free commands, the "lost serial" explanation, the claim that apply-time refresh is redundant, and the Verify steps.
Method: documentation only; no commands were run.
