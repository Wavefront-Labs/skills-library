---
id: computing-software.cloud-infrastructure-engineering.terraform.verifying-a-state-migration
name: verifying-a-state-migration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, migration-verification, state-migration, lineage-mismatch, backend-migration]
level: practitioner
status: docs-checked
description: "Prove a backend or workspace migration worked: back up state, compare old and new with state pull, run a no-op plan, and retire the old backend safely."
sources: ["https://developer.hashicorp.com/terraform/language/backend#changing-configuration", "https://developer.hashicorp.com/terraform/cli/commands/state/pull", "https://developer.hashicorp.com/terraform/cli/commands/plan#detailed-exitcode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying a state migration

When you change backends, `terraform init` offers to migrate the state to the new backend. Before migrating, HashiCorp strongly recommends backing up the state by copying it elsewhere.

## Before migrating
```bash
terraform state pull > pre.tfstate
jq '[.resources[].instances[]] | length' pre.tfstate
terraform plan -detailed-exitcode     # record: ideally exit 0
```
`state pull` downloads the state from its current location and prints the raw JSON to stdout (the docs suggest pairing it with `jq`). The output is always converted to the current Terraform version, so it cannot tell you the version of the remote state. State files must be UTF-8 without a BOM; on Windows PowerShell use `Set-Content` rather than `>`.

## After `init -migrate-state` (or API upload)
```bash
terraform state pull > post.tfstate
jq '[.resources[].instances[]] | length' post.tfstate
diff <(jq -S '.resources' pre.tfstate) <(jq -S '.resources' post.tfstate) && echo "resources identical"
terraform plan -detailed-exitcode     # must be exit 0 (or the same diff as before)
```
With `-detailed-exitcode`, exit 0 means succeeded with an empty diff, 1 means error, and 2 means succeeded with changes present.
Expect: same instance count and identical resources.

## Per-workspace
If you use multiple workspaces, Terraform detects them on a backend change and asks whether to copy all workspaces to the destination. Loop over `terraform workspace list` and repeat the comparison for each; workspaces are easy to miss.

## Red flags
| Symptom | Meaning |
|---|---|
| Plan wants to create everything | Pointing at an empty state/key; stop, do not apply |
| Instance count lower | A workspace or module missing; compare per workspace |
| Old backend still being written by a pipeline | CI not updated; two diverging states |

## Retire the old backend
1. Update every pipeline and developer config; rotate credentials of the old location.
2. Make old state read-only (bucket policy deny PutObject) for a grace period.
3. Delete after the grace period, keeping a final backup offline.

## Verify
- [ ] Instance counts match; plan is clean in every workspace.
- [ ] No writes to the old backend after cutover (access logs).

## Checked
2026-11-08. Confirmed against the Terraform backend configuration page (init asks to migrate state, copies all workspaces, back up state first), the `terraform state pull` page (raw output to stdout, jq pairing, always upgraded to current version, UTF-8 without BOM) and the `terraform plan` page (`-detailed-exitcode` codes 0, 1 and 2). Removed: serial and lineage comparison claims, which none of the cited pages document.
Method: documentation only; no commands were run.
