---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-state-lock-errors-and-lock-info
name: reading-state-lock-errors-and-lock-info
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lock-info, lock-error, state-locking, force-unlock, troubleshooting]
level: practitioner
status: docs-checked
description: "Handle Error acquiring the state lock: what state locking does, when force-unlock is safe, the lock ID nonce, and where the S3 backend keeps its lock."
sources: ["https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/cli/commands/force-unlock", "https://developer.hashicorp.com/terraform/language/backend/s3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading state lock errors

Example of the shape of the error (values are illustrative):

```
Error: Error acquiring the state lock

Error message: ... PreconditionFailed
Lock Info:
  ID:        6a1f0c3e-58e5-2a9d-61f6-2fd1b5d0a8a4
  Path:      <bucket>/<key>.tfstate
  Operation: ...
  Who:       <user>@<host>
  Version:   <terraform version>
  Created:   <timestamp>
```

## How locking behaves
- If the backend supports it, Terraform locks state for every operation that could write state. This happens
  automatically with no message. If locking fails, Terraform does not continue.
- If acquiring the lock takes longer than expected, Terraform prints a status message.
- Not every backend supports locking; the backend's own page says whether it does.
- `-lock=false` disables locking for most commands; the docs advise against it.

## The lock ID
`terraform force-unlock [options] LOCK_ID` removes the lock on the state for the current configuration. The lock ID is a
nonce: Terraform prints it when unlocking fails, and the command requires it so unlocks target the correct lock. The
only documented option is `-force` (skip the confirmation prompt). The command does not modify infrastructure. For a
local state file, the lock cannot be released by another process.

## Decision
1. Read the lock info first (who holds it, when it was created). If another run is genuinely in progress, wait for it.
2. Treat `force-unlock` as the last resort. The docs warn that unlocking while someone else holds the lock can cause
   multiple writers; it should only be used to release your own lock when automatic unlocking failed.
3. Before unlocking a lock you did not create, confirm the holder is gone (CI job cancelled, runner dead) using your own
   CI and host tooling.
4. After an interrupted apply, inspect the state and the real resources before the next apply.

## S3 backend specifics
- Setting `use_lockfile = true` enables locking in the S3 backend (default `false`). The lock file is `<key>.tflock` in
  the bucket; the identity needs `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on that object.
- `dynamodb_table` (deprecated) names a DynamoDB table used for locking; its partition key must be named `LockID` with
  type String.
- Look up other backends' locking behaviour on their own pages.

## Verify
- [ ] Lock holder identified before any unlock.
- [ ] After unlocking, a plan acquires and releases the lock normally.

## Checked

Checked 2026-11-08 against the Terraform State Locking page, the `terraform force-unlock` command page and the S3
backend page: automatic locking, `-lock=false`, the force-unlock warning, the lock ID nonce, `-force`, `use_lockfile`,
`.tflock` and its permissions, and the `dynamodb_table` deprecation and `LockID` key were confirmed. Removed (not stated
on the fetched pages): the per-field meaning table, the `OperationType*` values, `-lock-timeout`, the `errored.tfstate`
advice, DynamoDB item format, and GCS, azurerm and HCP Terraform lock details.

Method: documentation only; no commands were run.
