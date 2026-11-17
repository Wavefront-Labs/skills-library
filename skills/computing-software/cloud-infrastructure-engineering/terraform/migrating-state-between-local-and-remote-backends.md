---
id: computing-software.cloud-infrastructure-engineering.terraform.migrating-state-between-local-and-remote-backends
name: migrating-state-between-local-and-remote-backends
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, local-to-remote, migrate-local-state, remove-backend, migrate-to-local, migrate-state, bootstrap-backend]
level: practitioner
status: docs-checked
description: "Move local state into a remote backend (including the bootstrap-bucket case) and back to local, with init -migrate-state, -force-copy and -reconfigure explained."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#backend-initialization", "https://developer.hashicorp.com/terraform/language/backend#changing-configuration", "https://developer.hashicorp.com/terraform/cli/commands/state/pull", "https://opentofu.org/docs/cli/commands/init/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local and remote state migration

## Local to remote
1. Back up first. HashiCorp strongly recommends manually copying your `terraform.tfstate`
   file to another location before migrating:
   `cp terraform.tfstate terraform.tfstate.pre-migration`.
2. Add the backend block (one `backend` block per configuration, and it cannot refer to
   variables, locals or data sources). Leave credentials out of the block and supply them
   through the conventional environment variables or credentials files:
```hcl
terraform {
  backend "s3" {
    bucket = "acme-tf-state"
    key    = "network/terraform.tfstate"
    region = "eu-west-1"
  }
}
```
   Check the backend type's own page for further arguments such as locking options.
3. `terraform init -migrate-state` copies existing state to the new backend and may prompt
   to confirm migration of workspace states. `-force-copy` suppresses those prompts, answers
   "yes", and automatically enables `-migrate-state` (useful in CI).
4. Run `terraform plan` and confirm it reports no actions needed.
5. Once verified, archive or remove the local `terraform.tfstate*` files so nobody uses them by accident.

## Bootstrapping the backend's own storage
The storage must exist before it can hold state. Pattern:
1. A separate root (for example `bootstrap/`) creates the bucket (and anything else the backend needs), using local state.
2. Apply it.
3. Add the backend block pointing at that bucket and run `init -migrate-state`.
The bootstrap stack then keeps its state in the storage it manages.

## Remote to local
1. Remove the `backend` block and reinitialise. Terraform prompts you to migrate the state
   to the default local backend (the local backend stores state as a file on disk).
2. Run `terraform plan` to check. The remote object still exists; delete it only when sure.
A configuration with a `cloud` block cannot also have a `backend` block, and HCP Terraform
manages state in its workspaces.

`terraform state pull` downloads state from its current location, upgrades the local copy to
the latest state file version your Terraform can handle, and writes the raw state to
stdout; it is a way to take a copy before a risky change. State files must be UTF-8 without a
byte order mark: on Windows PowerShell pipe it through `Set-Content terraform.tfstate`
rather than using a redirect.

## Gotchas
- Changing backend configuration requires `terraform init` again, with either `-reconfigure`
  or `-migrate-state`.
- `-reconfigure` disregards any existing configuration and prevents migration of any existing
  state. It is not a migration; use `-migrate-state` when you want the state copied.
- If you use multiple workspaces, Terraform can copy all of them to the destination and asks
  whether you want that.
- Reconfiguring the same backend also asks whether to migrate state; you can answer "no".
- Stop CI (or otherwise avoid writes to the old state) during migration; this is process advice, not from the docs.
- `.terraform/` holds the backend configuration in plain text; do not commit it.
- OpenTofu's `tofu init` documents the same `-migrate-state`, `-force-copy` and `-reconfigure` behaviour.

## Checked
Date: 2026-11-07. Read in full: Terraform `init` command page (Backend Initialization section and the options), "Backend block configuration overview" (Initialize the backend, Partial configuration, Change configuration, Remove a backend configuration), `state pull` page and the OpenTofu `init` page. Confirmed: -migrate-state / -force-copy / -reconfigure semantics, back-up recommendation, one backend block and no named values, multi-workspace copy, remove-backend prompt, `cloud` and `backend` exclusivity, state pull behaviour and the BOM/PowerShell note. Trims: removed `use_lockfile` and other s3 arguments not on the cited pages, the quoted interactive prompt text, `prevent_destroy`/KMS/lock-table remarks, the "terraform init will not migrate back from cloud" procedure, the `jq '.lineage, .serial'` Verify step and the "credentials for both backends" claim. The s3 backend page and the cloud block page were not read.
Method: documentation only; no commands were run.
