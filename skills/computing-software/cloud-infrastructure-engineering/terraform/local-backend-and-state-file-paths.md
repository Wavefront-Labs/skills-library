---
id: computing-software.cloud-infrastructure-engineering.terraform.local-backend-and-state-file-paths
name: local-backend-and-state-file-paths
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, local-backend, local-state-path, terraform-tfstate, workspace-dir, state-file]
level: practitioner
status: gated
description: "Use the local backend deliberately: path and workspace_dir settings, terraform.tfstate.d layout, legacy -state flags, and when local state is acceptable."
sources: ["https://developer.hashicorp.com/terraform/language/backend/local", "https://developer.hashicorp.com/terraform/language/state/workspaces", "https://opentofu.org/docs/language/settings/backends/local/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The local backend

With no `backend` block Terraform uses `local` implicitly: `./terraform.tfstate`,
backup `./terraform.tfstate.backup`, workspaces under `./terraform.tfstate.d/<name>/` (`terraform.tfstate.d/staging/` seen after `workspace new`).

## Explicit configuration
```hcl
terraform {
  backend "local" {
    path          = "state/network.tfstate"   # relative to the root module dir
    workspace_dir = "state/workspaces"        # non-default workspaces
  }
}
```
Run `terraform init -migrate-state` after changing `path` so the state is copied to the new file
instead of starting empty. It is a copy: after migrating `state/network.tfstate` to `state/moved.tfstate` both files
held the resource (711 bytes each) and the old file was left in place, so delete or archive the old one yourself once the new
location is verified.

## When local state is fine
- Throwaway sandboxes, learning, `terraform test` runs, one-person tools.
- Bootstrapping the remote backend itself (the S3 bucket/lock resources) — then
  migrate it into the bucket it created.

## When it is not
Anything shared: no locking across machines, no history, secrets sit in plaintext
on a laptop, and a lost disk means rebuilding state (see the disaster-recovery skills).

## Legacy flags
`-state=path`, `-state-out=path`, `-backup=path` (or `-backup=-` to disable) still
work on `plan`/`apply`/`state *` **only with the local backend** (`state mv -help`: "legacy options supported for the local
backend only"). `apply -state=custom.tfstate` created `custom.tfstate`, and `-backup=-` produced no `.backup` file. Prefer
`path` in the block or a separate `TF_DATA_DIR`/working directory per state.

## Gotchas
- `.gitignore` must contain `*.tfstate`, `*.tfstate.*`, `.terraform/` — committing
  state leaks secrets and causes merge-conflicted state.
- Locking is a local OS file lock; two terminals on the same machine are protected (a `plan` during a running
  `apply` failed on Windows with `Error acquiring the state lock ... another process has locked a portion of the file`),
  two machines sharing a network drive are not reliably.
- `terraform.tfstate.d/` holds workspace state; deleting it deletes those workspaces.
- `path` is resolved relative to the working directory used for the run, so
  `-chdir` changes where it lands.

## Verify
- [ ] `terraform state pull | jq .serial` reads the file you expect.
- [ ] `git check-ignore -v terraform.tfstate` confirms state is ignored.
- [ ] After a change to `path`, the new file has the same lineage (the old file is still there until you remove it).

## Checked
- Terraform 1.17.0 on Windows with the local backend: default files `terraform.tfstate` and `.backup`; with `path = "state/network.tfstate"` and `workspace_dir = "state/workspaces"` the files were `state/network.tfstate`, `state/network.tfstate.backup` and `state/workspaces/dev/terraform.tfstate`; `-migrate-state -force-copy` after changing `path` copied (old file remained); `-state`, `-backup=-` and `-chdir` (state read from the `-chdir` directory) behaved as described; `git check-ignore -v` matched `terraform.tfstate` and `custom.tfstate` against the three-pattern `.gitignore`; the concurrent-run lock error reproduced.
- `state mv -help` quoted for the legacy flags.
- The network-drive locking statement (gated: unconfirmed, source is paywalled or blocked), the sandbox/bootstrap/`terraform test` suggestions, and the disaster-recovery references are advice or provider behaviour not exercised here (gated: unconfirmed, source is paywalled or blocked). The reason is that no remote backend or shared drive was available.
