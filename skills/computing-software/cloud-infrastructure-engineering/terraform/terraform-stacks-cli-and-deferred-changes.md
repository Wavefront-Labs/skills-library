---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-stacks-cli-and-deferred-changes
name: terraform-stacks-cli-and-deferred-changes
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, terraform-stacks, stacks-cli, deferred-changes, convergence-check, auto-approve, providers-lock]
level: advanced
status: docs-checked
description: "Operate Stacks from the CLI (terraform stacks init, validate, providers-lock, fmt, configuration upload) and understand deferred changes and convergence checks."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/stacks", "https://developer.hashicorp.com/terraform/cloud-docs/stacks/deploy/runs", "https://developer.hashicorp.com/terraform/language/stacks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stacks CLI and deferred changes

## CLI
```bash
terraform stacks init                     # download modules/sub-Stacks and providers; writes .terraform.lock.hcl
terraform stacks providers-lock           # create or update .terraform.lock.hcl
terraform stacks validate                 # validate config files without remote services
terraform stacks fmt                      # canonical format for component and deployment config
terraform stacks configuration upload     # upload current directory to a Stack not connected to VCS
terraform stacks deployment-run list ...  # manage deployment runs (also: approve-all-plans, cancel, watch)
```
Other commands: `create`, `list`, `version`; subcommand groups `deployment-run`,
`deployment-group` and `configuration`. Run `terraform stacks init` and
`terraform stacks providers-lock` before `validate`; the `.terraform` directory
should not be committed.

`configuration upload` targets a Stack by `-stack-id`, or by `-organization-name`,
`-project-name` and `-stack-name` (each has a `TF_STACKS_*` environment variable);
`-speculative` uploads without triggering deployments. On Terraform Enterprise set
`TF_STACKS_HOSTNAME` to the instance hostname.

## Deferred changes
When a component needs attributes from another component that do not exist yet,
HCP Terraform recognises the dependency and defers that step until it can
complete it. Approving a plan that contains deferred changes makes HCP Terraform
create a follow-up plan automatically; the UI notes when a plan has deferred
changes. A typical case is Kubernetes workloads that depend on a cluster created in
the same Stack.

Only certain providers and versions support deferred changes (for the Kubernetes
provider, 2.32.0 or later); check the provider's registry page.

## Convergence checks and approval
- After any applied step HCP Terraform runs a **convergence check**: a replan that
  confirms no component has deferred changes. It keeps replanning until the plan is
  empty.
- Every Stack has an `auto_approve` rule named `empty_plan` that auto-approves
  plans with no changes.
- Plans can be approved per deployment (**Approve plan**) or for a whole
  configuration version (**Approve all plans**), in the UI or with
  `terraform stacks deployment-run`.
- Custom auto-approval uses `deployment_auto_approve` blocks attached to a
  `deployment_group` through `auto_approve_checks`; the older `orchestrate` /
  `auto_approve` / `replan` blocks are deprecated.

## Gotchas
- `providers-lock` by default requests checksums for HCP Terraform (`linux_amd64`)
  and your current machine; add more with repeated `-platform=os_arch`.
- Deferral is a Stacks feature; ordinary root modules do not defer.

## Verify
- [ ] `terraform stacks validate` passes in CI on every PR.
- [ ] A greenfield deployment converges over successive plans.

## Checked
2026-11-09. Confirmed against the terraform stacks CLI pages (index, init, validate, providers-lock, configuration upload), the HCP Terraform "Review deployment runs" page (deferred changes, convergence checks, `empty_plan`), the Stacks use-cases and provider pages (Kubernetes provider 2.32.0), and the Stacks GA update page (deprecated orchestration blocks, `deployment_auto_approve`).
Removed as unsupported: the claim that the CLI began as a separate `tfstacks` binary and that command names changed between beta and GA; "plans run only in HCP Terraform, never locally"; `for_each` over post-apply values; the EKS two-plan walk-through; the `deferred-changes` source URL (404).
Method: documentation only; no commands were run.
