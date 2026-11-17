---
id: computing-software.cloud-infrastructure-engineering.terraform.backend-to-backend-migration-with-workspaces
name: backend-to-backend-migration-with-workspaces
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, migrate-state-flag, backend-to-backend, workspace-migration, migrate-workspaces, init]
level: advanced
status: docs-checked
description: "Migrate state between two remote backends (for example S3 to azurerm or gcs), including every workspace, with a state backup first and a plan check afterwards."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#backend-initialization", "https://developer.hashicorp.com/terraform/language/backend#initialization", "https://developer.hashicorp.com/terraform/language/state/workspaces", "https://developer.hashicorp.com/terraform/cli/workspaces", "https://developer.hashicorp.com/terraform/cli/commands/state/push", "https://opentofu.org/docs/cli/commands/init/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backend-to-backend migration (with workspaces)

## Plan the cut-over
1. Back up the state first. The backend docs "strongly recommend manually backing up your
   state" before migrating to a new backend. For each workspace, select it
   (`terraform workspace select NAME`) and save `terraform state pull > backup-NAME.tfstate`
   (`state pull` prints the raw state to stdout).
2. Tell collaborators not to run Terraform against the old backend meanwhile.
3. Supply credentials for the backends through the environment variables or credential
   files conventional for each system; the docs recommend against hard-coding
   credentials in the backend block or passing them with `-backend-config`.

## Run it
Edit the `backend` block to the new type or settings (a configuration may have only one
backend block, and it cannot refer to variables, locals or data sources):
```hcl
terraform {
  backend "gcs" {
    bucket = "example-tf-state"
    prefix = "network"
  }
}
```
```bash
terraform init -migrate-state
```
- Changing a backend's configuration requires running `terraform init` again. Terraform
  detects the change and asks whether to migrate existing state to the new
  configuration; you can change the backend type (for example from `consul` to `s3`) or
  only its settings. Reconfiguring the same backend still asks; you can answer "no".
- With multiple workspaces, Terraform can copy all of them to the destination, and asks
  if that is what you want.
- `-migrate-state` copies existing state to the new backend and may prompt to confirm
  workspace migration. `-force-copy` suppresses those prompts, answers "yes", and
  enables `-migrate-state` automatically.
- `-reconfigure` disregards the existing configuration and prevents migration of
  existing state.
- Multiple workspaces are supported by these backends: AzureRM, Consul, COS, GCS,
  Kubernetes, Local, OSS, Postgres, Remote and S3. The `default` workspace cannot be deleted.
- OpenTofu's `tofu init` documents the same `-migrate-state`, `-force-copy` and
  `-reconfigure` behaviour.

## Verification per workspace
For each workspace, `terraform workspace select NAME`, then:
```bash
terraform plan -detailed-exitcode
```
Exit code 0 means succeeded with no changes, 1 an error, 2 changes present.

## Rollback
Keep the pulled backup files. `terraform state push PATH` uploads a state file to the
configured backend; it refuses a state whose lineage differs or whose serial is lower than
the destination's, unless you pass `-force`, which the docs say is not recommended.

## Checked
Date: 2026-11-07

Read in full (stripped text): `terraform init` (backend initialization), "Backend block configuration overview" (initialization, partial configuration, change configuration, remove backend), "Workspaces" and "Manage Workspaces Overview", `terraform state push`, `terraform plan`, and OpenTofu's `init` page. No code tabs were present.

Trimmed as unconfirmed: the freeze via Atlantis/pipelines; recording `serial`/`lineage` per workspace; the "Do you want to migrate all workspaces to gcs" prompt text; the claim that a destination supporting only `default` (for example `http`) asks which workspace to migrate; the inline workspace-rename recipe; the loop with `tr` and `jq`; `-lock=false` on the verification plan (the plan page calls it dangerous); "migration never deletes the source" and the rollback by restoring the old block; the three Gotchas (lost concurrent writes, `terraform_remote_state` consumers, lineage unchanged); both Verify steps. Added the backend overview, CLI workspaces and `state push` pages to `sources`.

Method: documentation only; no commands were run.
