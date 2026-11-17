---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.state-management-locking-and-backends
name: state-management-locking-and-backends
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, state-management, remote-state, state-locking, state-backend, terraform-state, opentofu, s3-backend, dynamodb-lock, s3-lockfile, azurerm-backend, gcs-backend, hcp-terraform, pulumi-state, pulumi-backend, state-encryption, state-isolation, state-per-environment, workspaces, state-move, state-rm, import, force-unlock, terraform-state-list, stack-references, remote-state-data-source, state-secrets, state-backup]
level: advanced
status: docs-checked
description: "Design Terraform/OpenTofu state: remote backends per environment with locking (S3, azurerm, GCS), isolation boundaries, secrets in state, state surgery and recovery."
sources: ["https://developer.hashicorp.com/terraform/language/backend/s3", "https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://developer.hashicorp.com/terraform/language/backend/gcs", "https://developer.hashicorp.com/terraform/language/state/remote-state-data", "https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/cli/commands/force-unlock", "https://developer.hashicorp.com/terraform/cli/commands/state/mv", "https://developer.hashicorp.com/terraform/cli/commands/state/rm", "https://developer.hashicorp.com/terraform/cli/workspaces", "https://developer.hashicorp.com/terraform/language/block/import", "https://opentofu.org/docs/language/state/encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State management, locking and backends

**Goal:** state is remote, locked, versioned, encrypted, small enough to plan in
seconds, and split so a mistake in one stack cannot touch another environment.

## 1. Backend per tool
```hcl
# Terraform / OpenTofu: S3 backend with native lockfile
terraform {
  backend "s3" {
    bucket       = "acme-tfstate-prod"
    key          = "network/eu-west-1/terraform.tfstate"
    region       = "eu-west-1"
    use_lockfile = true           # dynamodb_table is deprecated
    encrypt      = true
    kms_key_id   = "<KMS_KEY_ARN>"
  }
}
```
- S3 `use_lockfile` defaults to false; with it set, `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` are needed on the `.tflock` object. The deprecated `dynamodb_table` lock table needs a string partition key named `LockID`.
- Azure: `azurerm` backend (see its page for authentication options such as Azure AD).
- GCS: `gcs` backend; enable object versioning on the bucket.
- OpenTofu: an `encryption` block with key providers (for example `aws_kms`, `pbkdf2`) and the AES-GCM method gives client-side encryption of state.
- CloudFormation/Bicep: the cloud holds state; your concern is drift detection, not storage.

Bucket hygiene: versioning on, public access blocked, access limited to the CI role plus break-glass, retention that
covers your recovery window, access logging.

## 2. Isolation: how to split state
Rule: **blast radius x change frequency**. Separate state for things that change at
different cadences or that must never be destroyed together.
```
network/        (rarely changes, many dependants)      -> own state per env/region
platform/eks/   (cluster lifecycle)                     -> own state
data/rds/       (stateful, deletion-protected)          -> own state
apps/<app>/     (frequent)                              -> own state per app per env
```
Environments: separate **backends or at least separate keys and credentials** per env, not
Terraform workspaces alone (workspaces share the backend and its credentials; a
`-target` typo in the wrong workspace is one keystroke away). Directory-per-env with a shared
module keeps the files small and the state names explicit.

Cross-stack reads: `data "terraform_remote_state"` (needs read access to the whole state, so
it exposes everything in it) or, better, publish outputs to a parameter store or secrets manager
and read those.

## 3. Secrets in state
Terraform state stores resource attributes in plain JSON, including passwords and keys
returned by providers. Treat the backend as a secret store: encryption, tight IAM, no
`terraform state pull` output into tickets. Reduce exposure: ephemeral values (Terraform 1.10 or later),
`sensitive = true` on outputs (hides from CLI output, not from state), generate secrets outside and reference them.

## 4. State surgery (safe order)
```bash
terraform state list                         # see what is tracked
terraform state show aws_instance.web        # one resource
terraform state pull > backup.tfstate        # always first; keep until the change is verified
terraform state mv module.old.aws_sg.x module.new.aws_sg.x    # refactor without destroy (or `moved {}` blocks in code, preferred: reviewable)
terraform state rm aws_iam_role.legacy       # forget without destroying
terraform import aws_s3_bucket.logs acme-logs  # or `import {}` blocks + `terraform plan -generate-config-out=generated.tf`
terraform force-unlock <LOCK_ID>             # only when the holder is dead; check the run queue first
```
`moved` and `import` blocks are code, so they go through review and apply once;
CLI commands change state immediately with no plan. Prefer the blocks.

## 5. Recovery
- Corrupted or partial apply: pull the state, compare with the previous object version in the bucket, restore it, then `terraform plan` to see the delta against reality and import or remove what differs.
- Lost state entirely: re-import everything (slow). This is why bucket versioning is non-negotiable.
- Lock stuck after a CI job was killed: confirm no process holds it, then `force-unlock`.
- State too large (minutes to refresh): split stacks; `-refresh=false` for emergency plans; `-target` only in exceptional circumstances such as recovering from mistakes, never routine.

## Gotchas
- `terraform init -migrate-state` moves state when you change backends. Read the prompt.
- Two pipelines pointing at the same `key` is a classic incident; name keys after the directory path and lint for duplicates.
- With workspaces, non-default workspace state in S3 lives under `<workspace_key_prefix>/<workspace_name>/<key>`, where the prefix defaults to `env:`. Account for it in bucket policies.
- `terraform_remote_state` requires the caller to be able to read the whole state; it is read access to every secret in it.

## Verify
- [ ] `terraform init` from a clean clone configures the remote backend with no local `terraform.tfstate` created.
- [ ] Two concurrent `terraform plan`s show one waiting on the lock; a killed run's lock can be cleared with `force-unlock`.
- [ ] Bucket shows versioning on, encryption on, public access blocked, and an older state version can be restored in a drill.
- [ ] Each environment uses distinct credentials: prod state is unreadable with the stage CI identity.

## Checked
2026-11-01. Confirmed in the Terraform S3, azurerm, GCS, remote state data, locking, force-unlock, state mv/rm/list, workspaces, import and sensitive-data pages and the OpenTofu state encryption page: `use_lockfile` (default false), deprecated `dynamodb_table` with `LockID`, lockfile permissions, workspace key prefix `env:`, `-migrate-state`, `-generate-config-out`, `-refresh=false` and `-target` guidance, OpenTofu `encryption` block with `aws_kms`, `pbkdf2` and AES-GCM, ephemeral values from Terraform 1.10. Removed: Pulumi backend and StackReference lines, the HCP `cloud {}` line, Terragrunt, the 90-day retention figure, object lock, terraformer/aws-nuke, `-reconfigure` and the lockfile conditional-write claim.
Method: documentation only; no commands were run.
