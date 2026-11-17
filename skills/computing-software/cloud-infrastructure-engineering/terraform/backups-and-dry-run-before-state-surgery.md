---
id: computing-software.cloud-infrastructure-engineering.terraform.backups-and-dry-run-before-state-surgery
name: backups-and-dry-run-before-state-surgery
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-dry-run, surgery-backup, state-mv, state-rm, state-manipulation]
level: practitioner
status: docs-checked
description: "Make state surgery reversible: pull a backup, use state mv/rm -dry-run, apply the change, verify with a plan using -detailed-exitcode, and know how state push -force rolls back."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/mv", "https://developer.hashicorp.com/terraform/cli/commands/state/rm", "https://developer.hashicorp.com/terraform/cli/commands/state/push", "https://developer.hashicorp.com/terraform/cli/commands/state/pull", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe state surgery: backup and dry-run

## Runbook
```bash
# 0. Coordinate: nobody else changes configuration or state meanwhile
# 1. Baseline
terraform plan -detailed-exitcode        # exit 0 = no changes, 1 = error, 2 = changes
terraform state pull > backup-before.tfstate

# 2. Dry-run every operation
terraform state mv -dry-run 'aws_instance.web' 'module.web.aws_instance.this'
terraform state rm -dry-run 'aws_iam_role_policy_attachment.legacy'

# 3. Execute (same commands without -dry-run)
terraform state mv 'aws_instance.web' 'module.web.aws_instance.this'

# 4. Verify: the plan should show only the changes you intended
terraform plan -detailed-exitcode
```
- `state pull` downloads the state from its current location (remote or local), upgrades the
  copy to the latest state file version your Terraform supports, and prints the raw
  format to stdout. It cannot show the Terraform version of the remote state, because
  output is always converted to the current version.
- `-dry-run` on `state mv` and `state rm` reports the matching resource instances
  without changing state ("forgetting" none of them).
- `state mv SOURCE DESTINATION` rebinds an existing remote object to a new address; the
  source and destination must be the same kind of object (instance to instance, module
  instance to module instance), and a resource can only move to an address with the
  same resource type. Without it, a rename in configuration is read as delete and create.
- `state rm ADDRESS...` removes the binding without destroying the remote object. A
  later plan will propose creating a new object for each forgotten instance, and that
  can fail if names or identifiers conflict with the objects still present.
- `-lock=false` skips the state lock and is dangerous if others might run commands on the
  same workspace; `-lock-timeout=DURATION` retries lock acquisition.
- In a collaborative environment, the `state mv` docs warn to make sure nobody makes other
  changes between your configuration change and the `state mv`, or they could create a
  plan that destroys the old object and creates a new one.

## Rollback
```bash
terraform state push backup-before.tfstate
```
`state push PATH` uploads a state file to the configured backend (`-` reads stdin) and
refuses if the lineage differs or the destination serial is higher than the pushed
state. `-force` disables both checks, and the docs say that is not recommended because
the destination state is overwritten. HashiCorp recommends `state push` only when you
must manually modify the remote state. Files must be UTF-8 without a byte order mark.

## Prefer config-driven removal
The `state rm` page says `removed` blocks can replace it: you can remove several resources
at once and review the removals in the normal plan and apply workflow.

## Gotchas
- Quote addresses containing brackets, because brackets have special meaning in some
  shells: `'aws_instance.web["a"]'` on Unix-style shells; the docs show different quoting
  for Windows `cmd.exe` and PowerShell.
- `-backup` and `-backup-out` on `state mv` are legacy options that operate on a local
  state file only; with the remote backend you must supply a local file via `-state`.

## Checked
Date: 2026-11-07

Read in full (stripped text): `terraform state mv`, `state rm`, `state push`, `state pull`, and `terraform plan` (the `-detailed-exitcode` and `-out` options). I did not open any code tab or linked tutorial.

Trimmed as unconfirmed: the `jq` serial/lineage step; "Would move / Would remove" output text; "Every state command writes a new serial"; "backup written locally only for the local backend" (the page only says `-backup` is legacy and local-only); the claim that `moved`/`import` blocks are always preferable; "batch many moves in one script"; the `plan -out=before.tfplan` step and both Verify checkboxes (replaced by the plan with `-detailed-exitcode`, whose exit codes the plan page lists). Added `state pull` and `plan` to `sources`.

Method: documentation only; no commands were run.
