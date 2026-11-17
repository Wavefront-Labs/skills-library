---
id: computing-software.cloud-infrastructure-engineering.terraform.stale-locks-force-unlock-and-lock-false
name: stale-locks-force-unlock-and-lock-false
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, force-unlock-procedure, stale-lock, lock-false, disable-locking, workspace-lock, hcp-workspace-lock, lock-timeout]
level: practitioner
status: docs-checked
description: "Clear a stale state lock safely with force-unlock (or an HCP workspace unlock), know when -lock=false is acceptable, and use -lock-timeout to avoid both."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/force-unlock", "https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings#locking", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#force-unlock-a-workspace", "https://developer.hashicorp.com/terraform/language/backend/s3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stale locks, `force-unlock`, and `-lock=false`

## 1. What locking does
If the backend supports it, Terraform locks state automatically for all operations that
could write state. If locking fails Terraform does not continue. When acquiring the lock
takes longer than expected, Terraform prints a status message. Not all backends support
locking; each backend's page says whether it does.

## 2. Procedure before unlocking
`terraform force-unlock` should only be used to unlock **your own** lock when automatic
unlocking failed. Unlocking while someone else holds the lock "could cause multiple
writers".
1. Find the holder: is a CI job, Atlantis run or teammate's terminal still running?
2. If it is running, **wait** (or cancel it cleanly so it releases the lock).
3. If it died (killed runner, laptop closed), confirm no process is still writing: a
   half-finished apply that resumes after you unlock will race you.
4. Unlock with the exact lock ID, which Terraform outputs when unlocking fails and which
   acts as a nonce so the unlock targets the correct lock:
```bash
terraform force-unlock LOCK_ID           # asks for confirmation
terraform force-unlock -force LOCK_ID    # -force: do not ask for input
```
`force-unlock` removes the lock only; it does not modify infrastructure. How the lock
behaves depends on the backend, and local state files cannot be unlocked by another
process.
5. Run `terraform plan` and check whether the dead run left partial changes.

Backend specifics (S3): with `use_lockfile = true` (default false) the lock is an object
named `<key>.tflock`, and the IAM principal needs `s3:GetObject`, `s3:PutObject` and
`s3:DeleteObject` on it. The deprecated DynamoDB lock uses a table whose partition key is
`LockID` (type String).

## 3. HCP Terraform workspace locks
Locking a workspace prevents all applies (and many kinds of plans) from proceeding,
whether started from the UI, CLI, API or automation; a user must unlock it to enable
runs again. Users with lock/unlock permission cannot unlock a workspace locked by
another user, but users with admin access can force unlock. Locks are managed with a
single "Lock/Unlock/Force unlock" button (confirmation is requested when unlocking), also
available from the Actions menu. The API has `POST /workspaces/:workspace_id/actions/lock`,
`.../actions/unlock` and `.../actions/force-unlock`; only users with admin access can
force unlock through the API.

## 4. `-lock=false`
"Don't hold a state lock during the operation. This is dangerous if others might
concurrently run commands against the same workspace." HashiCorp does not recommend
disabling locking. Keep it for commands that cannot write state and that you know
nobody else is changing; never on `apply` or other state-writing commands.

## 5. Prefer `-lock-timeout`
`terraform apply -lock-timeout=10m` retries acquiring the lock for that duration before
returning an error (a number plus a unit letter, e.g. `3s`). That avoids most failures
caused by overlapping CI jobs. Serialise pipelines per state so locks are rarely
contended.

## Checked
Date: 2026-11-07
Read in full: "State Locking", `terraform force-unlock`, the S3 backend page, and the plan page's `-lock`/`-lock-timeout` text. HCP Terraform workspace settings page: read only the Locking section (matched lines). Workspaces API page (about 130 KB): read only the endpoint index, the Requirements list and the "Force Unlock a workspace" section, not the whole page.
Confirmed: items quoted above, including the force-unlock role, nonce wording, `-force`, admin-only force unlock, API paths, `.tflock` and `use_lockfile`/DynamoDB `LockID` details.
Removed (not on the pages): the sample Lock Info block and field semantics, `OperationType` values, Atlantis/pg/kubernetes/GCS/azurerm lock claims, "deleting the lock file equals force-unlock", "queued runs start once unlocked", "(needs admin)" for non-force API calls, the "lost update/diverged serial" explanation and the Verify steps.
Method: documentation only; no commands were run.
