---
id: computing-software.cloud-infrastructure-engineering.terraform.recovering-from-errored-tfstate-and-backup-files
name: recovering-from-errored-tfstate-and-backup-files
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, errored-tfstate, tfstate-backup, backup-file, state-push, disaster-recovery, state-recovery]
level: advanced
status: docs-checked
description: "Recover when Terraform cannot persist state to a backend: the locally written state, state pull and push, lineage and serial safety checks, -force, and force-unlock."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/push", "https://developer.hashicorp.com/terraform/language/state/backends", "https://developer.hashicorp.com/terraform/cli/state/recover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State that could not be written to the backend

## What Terraform does
With a non-local backend, Terraform does not normally persist state on disk. If
writing the state to the backend fails with a non-recoverable error, Terraform writes
the state locally to prevent data loss. Once the error is fixed the user must push
that state to the remote backend manually. The cited pages do not give the local
file's name; look in the working directory where the command ran, and copy the file
aside before running anything else.

## Documented recovery workflow
1. Unlock Terraform only if an apply or another process ended before releasing its
   lock. Unlocking overrides the protection against two processes modifying state at
   once; HashiCorp does not recommend it until you know what caused the lock to
   stick (see the `terraform force-unlock` command page).
2. Read state with `terraform state pull`, which prints the remote state to stdout;
   redirect it to a file for a backup.
3. Write state with `terraform state push PATH`, which uploads a local state file to
   the configured backend. If PATH is `-`, the state is read from stdin, loaded fully
   into memory and verified before it is written.

## Safety checks on push
Terraform refuses to push when:
- the lineage differs (a differing lineage suggests completely different states and
  possible data loss), or
- the destination state has a higher serial than the state being pushed (the
  destination holds data not in your local copy).

`-force` disables both checks and overwrites the destination state. This is not
recommended; even with `-force`, take a backup first with `terraform state pull`.
`terraform state push` is described as extremely dangerous: use it only when you must
manually modify remote state.

## Details
- State files must be UTF-8 without a byte order mark. On Windows PowerShell, the
  push page says to use `Set-Content` so the file is encoded as UTF-8.
- For configurations using the HCP Terraform CLI integration or the remote backend,
  `state push` also accepts `-ignore-remote-version`.
- Locking is optional and backend-dependent; the backend's own documentation says
  whether it supports locking.

## Checked
Date: 2026-11-07
Read in full: the terraform state push command page, the State Storage and Locking
page (backends overview) and the Recover state from backup overview.
Removed because the pages do not state them: the `errored.tfstate` file name and
the sample error text, the claim that `terraform.tfstate.backup` is written before
each state write, timestamped backups from state commands, per-cloud versioning
restore commands (`aws s3api get-object` and others), the HCP Terraform rollback
button, CI artifact advice, `cp` and `rm` commands and the Verify checklist.
Method: documentation only; no commands were run.
