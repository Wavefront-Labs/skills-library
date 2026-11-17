---
id: computing-software.cloud-infrastructure-engineering.terraform.workspace-show-list-and-the-default-workspace
name: workspace-show-list-and-the-default-workspace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, workspace-show, workspace-list, default-workspace, cli-workspaces, workspace-delete]
level: practitioner
status: gated
description: "Script around CLI workspaces with workspace show and list, guard against applying in the wrong one, and know the rules for the default workspace and deleting workspaces."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/workspace/show", "https://developer.hashicorp.com/terraform/cli/commands/workspace/list", "https://developer.hashicorp.com/terraform/cli/commands/workspace/delete"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `workspace show`, `list` and the default workspace

## Scripting
```bash
terraform workspace show                    # prints the current name, e.g. "prod"
terraform workspace list                    # current marked with *
terraform workspace select -or-create staging   # TF 1.4+: select, creating if missing
```
Guard in wrapper scripts before apply:
```bash
want=$1
[ "$(terraform workspace show)" = "$want" ] || { echo "in workspace $(terraform workspace show), expected $want"; exit 1; }
```
In CI prefer `TF_WORKSPACE=prod` (overrides the selected workspace for that process, even when
`.terraform/environment` says another one; it did not rewrite that file) so no local selection state is involved.
With the local backend a `plan` under `TF_WORKSPACE=prod` created the missing `prod` workspace
(it appeared in `workspace list` afterwards), so a typo in the variable creates a new empty workspace.

## The default workspace
- Always exists; cannot be deleted (`terraform workspace delete default` printed `Cannot delete the default workspace`, exit 1).
- With S3, its state is at `key`; other workspaces at `<workspace_key_prefix>/<name>/<key>`
  (default prefix `env:`).
- Many teams leave `default` empty and never use it, so an accidental apply in the
  wrong place is obvious (a plan that creates everything). Some add a check:
```hcl
locals { _guard = terraform.workspace == "default" ? file("ERROR: select a workspace") : null }
```
  (forces an error when run in default; crude but effective.)

## Deleting workspaces
```bash
terraform workspace select default
terraform workspace delete feature-x        # refuses if its state has resources: "Error: Workspace is not empty"
terraform workspace delete -force feature-x # deletes anyway ("WARNING: ... was non-empty"); resources become orphans
```
Destroy the resources first (`terraform workspace select feature-x && terraform destroy`).
You cannot delete the workspace you are in (`You cannot delete the currently active workspace`).

## HCP Terraform with the cloud block
With the `cloud` block, `workspaces.tags` links the working directory to existing HCP Terraform workspaces
whose tags match, and `workspaces.name` links it to one workspace (cloud-block settings docs). How each
`terraform workspace` subcommand behaves there is not covered here; check the HCP Terraform documentation.

## Verify
- [ ] Wrapper scripts assert the workspace before apply.
- [ ] No resources live in `default` (unless intended).

## Checked
- Terraform 1.17.0, local backend: `workspace show` printed `default`, `list` marked `* default`; `select -or-create staging` created and switched (`.terraform/environment` held `staging`, state under `terraform.tfstate.d/staging`); `TF_WORKSPACE=prod terraform workspace show` printed `prod` while the file said `staging`; deleting `default` failed; deleting a workspace with resources failed with `Workspace is not empty`; `-force` deleted it with the orphan warning; deleting the active workspace failed. The `-or-create` flag's version: the Terraform 1.4 changelog lists "A new `-or-create` flag was added to `terraform workspace select`".
- S3 backend docs fetched: other workspaces are stored at `<workspace_key_prefix>/<workspace_name>/<key>`, default prefix `env:` (example path `env:/development/path/to/my/key`). HCP docs fetched for tags and name.
- The `locals` guard that calls `file("ERROR: ...")` and the shell wrapper snippet were not run, and the S3 state layout was read from docs only (gated: unconfirmed, source is paywalled or blocked). The reason is that no S3 bucket was available.
