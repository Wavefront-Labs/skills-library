---
id: computing-software.cloud-infrastructure-engineering.terraform.workspace-and-environment-strategy
name: workspace-and-environment-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-workspaces, cli-workspaces, hcp-terraform-workspaces, terraform-cloud, environments, multi-environment, dev-stage-prod, tfvars, partial-backend-config, backend-config, terragrunt, ephemeral-environments, preview-environments, workspace-key-prefix, tf-workspace, environment-parity]
level: practitioner
status: docs-checked
description: "Choose how Terraform represents dev/stage/prod: CLI workspaces vs directory-per-env vs tfvars with partial backend config vs Terragrunt, and when workspaces suit ephemeral copies."
sources: ["https://developer.hashicorp.com/terraform/cli/workspaces", "https://developer.hashicorp.com/terraform/language/backend", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://developer.hashicorp.com/terraform/cli/commands/workspace/select", "https://developer.hashicorp.com/terraform/cli/commands/workspace/delete", "https://developer.hashicorp.com/terraform/cli/config/environment-variables", "https://developer.hashicorp.com/terraform/language/backend/s3", "https://developer.hashicorp.com/terraform/language/block/resource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform workspace and environment strategy: one pattern, chosen on purpose

**Goal:** pick a single, explicit way to represent environments so that nobody can
apply stage code to prod by forgetting a command, and differences between
environments are visible in review. Promotion of plans between environments is in
`computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion`.

## 1. Two different things called "workspace"
- **CLI workspace** (`terraform workspace new/select/list/delete`): separate instances of
  state data inside the same working directory and the same backend. Every initialized
  directory starts with a workspace named `default`; only one is selected at a time and most
  commands act on the selected one. Code can read `terraform.workspace`.
- **HCP Terraform workspace**: each has its own configuration, variable values, state, run
  history and settings, acting like a separate working directory. When the CLI is integrated
  with HCP Terraform, `terraform workspace` commands select the remote workspace.

HashiCorp's own advice: workspaces are not required, and complex deployments needing
separate credentials and access controls should use alternatives.

## 2. The options
| Pattern | How environments differ | Good for | Weak at |
|---|---|---|---|
| CLI workspaces | `terraform.workspace` plus per-workspace input variables | a parallel copy of one set of infrastructure to test a change (feature-branch copies) | strong isolation: same backend, so same credentials and access controls |
| Directory per env calling shared modules | each root module: a backend config plus a few module blocks with small differences | long-lived envs with different backends, credentials and access | some duplication of wiring |
| One root + `env/*.tfvars` + partial backend config | `-var-file` and `-backend-config` | uniform envs | easy to pair the wrong tfvars with the wrong backend |
| Terragrunt | per-env/component config with generated backend config | many components x many envs | extra tool with its own semantics |
| HCP Terraform workspaces | per-workspace variables and settings | teams already on HCP Terraform | vendor coupling |

The CLI workspaces page itself says CLI workspaces are not a suitable isolation mechanism
between development stages or teams, because they share one backend; its alternative is
reusable modules plus a separate configuration (with its own backend) per deployment.
Default recommendation here: **directory per environment** for prod-like environments,
**CLI workspaces only for throwaway copies**.

## 3. tfvars + partial backend config done safely
A partial configuration leaves backend arguments out (empty values in the `backend` block)
and supplies them at `terraform init` with `-backend-config=PATH` (a file) or
`-backend-config="KEY=VALUE"`.
```bash
terraform init -reconfigure -backend-config=env/prod.backend.hcl
terraform plan -var-file=env/prod.tfvars -out=tfplan
```
- Re-running `init` with changed backend settings requires `-reconfigure` or `-migrate-state`.
  `-reconfigure` disregards the existing configuration and prevents migration of existing
  state; `-migrate-state` copies existing state to the new backend and may prompt about
  workspace states. Pick deliberately, and back up state before migrating.
- Do not put credentials in `-backend-config`: Terraform writes backend configuration in
  plain text to `.terraform/terraform.tfstate` and into plan files; use environment
  variables for credentials. Shells keep command-line flags in history, so avoid
  `KEY=VALUE` for secrets.
- Wrap both commands in one script or Makefile target that takes `ENV` and derives both
  files from it, and add a guard in the configuration (resource `precondition` blocks are
  supported):
```hcl
variable "environment" { type = string }
data "aws_caller_identity" "me" {}
locals { expected_account = { prod = "<PROD_ACCOUNT_ID>", stage = "<STAGE_ACCOUNT_ID>" } }
resource "terraform_data" "guard" {
  lifecycle {
    precondition {
      condition     = data.aws_caller_identity.me.account_id == local.expected_account[var.environment]
      error_message = "Credentials do not match environment ${var.environment}."
    }
  }
}
```

## 4. Ephemeral environments with CLI workspaces
```bash
WS="pr-${PR_NUMBER}"
terraform workspace select -or-create "$WS"
terraform apply -auto-approve -var="name_suffix=${WS}"
# on PR close:
terraform destroy -auto-approve && terraform workspace select default && terraform workspace delete "$WS"
```
- `select -or-create` creates the workspace if it does not exist.
- `terraform workspace delete` refuses to delete the current workspace or one still tracking
  resources unless `-force` is given, which leaves the resources dangling (still existing,
  no longer managed). Destroy first, as above.
- `TF_WORKSPACE` can select the workspace instead of `terraform workspace select`; the docs
  recommend it only for non-interactive use, since in a local shell it is easy to forget it
  is set and apply to the wrong state.
- Derive every globally unique name (buckets, DNS) from `terraform.workspace`.
- Run a scheduled reaper that destroys workspaces whose PR is closed; orphaned previews cost money.

## 5. Keep differences reviewable
- Differences between envs should be data (instance sizes, counts, feature flags), not
  `terraform.workspace == "prod"` branching scattered through the code.
- Keep env-specific values in one file per env and diff them in review:
  `diff env/stage.tfvars env/prod.tfvars`.

## Gotchas
- The S3 backend stores the default workspace at `key` and other workspaces at
  `<workspace_key_prefix>/<workspace_name>/<key>`; the default prefix is `env:`
  (for example `env:/development/path/to/my/key`).
- With local state, workspace states live in `terraform.tfstate.d`; treat it like
  `terraform.tfstate`. Terraform stores the current workspace name locally in the ignored
  `.terraform` directory. Workspace names must be valid in a URL path segment without escaping.
- Workspaces are a shared resource, not private, unless you use only local state.
- Terragrunt `run --all apply` across environments in one command has a large blast radius;
  scope it to one environment directory (see `terragrunt-dry-multi-environment-configs`).

## Verify
- [ ] The team can state, in one sentence, which pattern represents environments here.
- [ ] Running with prod tfvars and stage credentials fails at plan via the guard.
- [ ] No resource uses `terraform.workspace` for prod-vs-nonprod logic.
- [ ] Ephemeral workspaces are destroyed and deleted on PR close; a reaper lists none older than N days.
- [ ] CI logs print the environment, backend key and account ID before every apply.

## Checked
Checked 2026-11-08 against HashiCorp's Manage Workspaces overview, backend configuration (partial configuration), `init`, `workspace select`, `workspace delete`, environment variables (`TF_WORKSPACE`), S3 backend and resource (`precondition`) pages.
Removed: the minimum Terraform versions quoted for `terraform_data` and `-or-create`, "default workspace cannot be deleted", the `terraform workspace show` advice, the Terraform Stacks row and the claim that mixing `TF_WORKSPACE` and `select` misbehaves, none of which the pages state. Corrected the backend-switch gotcha to the documented `-reconfigure` / `-migrate-state` behaviour.
Method: docs-only read of cited pages, 2026-11-08
