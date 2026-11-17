---
id: computing-software.cloud-infrastructure-engineering.terraform.interrupting-apply-and-recovering-partial-applies
name: interrupting-apply-and-recovering-partial-applies
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, apply-interrupt, sigint, interrupted-apply, partial-apply-recovery, terraform-apply]
level: practitioner
status: docs-checked
description: "What the docs say happens when a terraform apply errors or is canceled, how state locks and force-unlock work, and how to recover from a partially completed apply."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/cli/commands/force-unlock", "https://developer.hashicorp.com/terraform/cloud-docs/run/manage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupting `apply` and recovering

## When an apply errors
Per the apply command page, on an error Terraform logs and reports it, updates the state
file with any changes to your resources, unlocks the state, and exits. It does not roll
back a partially completed apply; after fixing the error you must apply again to bring
infrastructure to the desired state. Your infrastructure may be in an invalid state in
between, so run `terraform plan` before anything else.

## Canceling a run in HCP Terraform
Cancel Run is documented as roughly equivalent to Ctrl+C on the CLI: the Terraform
process gets an INT signal, ends its work, updates state for resources already changed,
and wraps up in the safest way possible. If a canceled run will not end and keeps the
workspace locked, Force Cancel Run terminates the process immediately and unlocks the
workspace; it needs workspace admin access and can cause loss of state and orphaned
resources. The button appears only after Cancel Run has been clicked and HCP Terraform
has had time to stop the run safely. Always cancel first, force only if it hangs.

## State locks
- Terraform locks state for operations that could write it, if the backend supports
  locking (not all do). If locking fails, Terraform does not continue.
- If locking is slow Terraform prints a status message. `-lock-timeout=DURATION` (for
  example `3s`) retries acquiring the lock before erroring. `-lock=false` skips locking
  and is dangerous if others may run against the same workspace.
- If unlocking failed, Terraform prints a lock ID. `terraform force-unlock LOCK_ID`
  removes the lock (add `-force` to skip the confirmation prompt). It does not modify
  infrastructure. Use it only for your own lock after automatic unlocking failed;
  unlocking while someone else holds the lock can create multiple writers. Local state
  files cannot be unlocked by another process.

## Recovery sequence from the docs
1. Resolve the cause of the error or interruption.
2. If the lock is stuck and you are sure nobody else is running, `force-unlock` it.
3. Run `terraform plan` to see what remains, then `terraform apply` again.
4. Avoid `-auto-approve` as a shortcut here: review the plan first, since a recovery
   plan can include destructive actions.

## Checked
Date: 2026-11-07
Read in full: terraform apply (cli/commands/apply), State Locking (language/state/locking), terraform force-unlock (cli/commands/force-unlock), and Manage and view runs (cloud-docs/run/manage, added to sources for the cancel behaviour).
Confirmed: apply error handling and no-rollback statement; lock behaviour and -lock/-lock-timeout flags; force-unlock usage, -force, warnings; HCP cancel and force-cancel behaviour; the -auto-approve note on destructive operations (apply page).
Removed: the "Interrupt received... Gracefully shutting down" message, the second-Ctrl-C and SIGKILL consequences, the `timeout -s INT` CI advice, "writes state after each resource", `errored.tfstate` and `terraform state push`, taint/untaint steps, `default_tags` and maintenance-window advice, the import-orphans advice, and the Verify checklist (none on the cited pages).
Not opened: the Apply Terraform Configuration tutorial the apply page links to for error recovery, and backend-specific locking pages.
Method: documentation only; no commands were run.
