---
id: computing-software.cloud-infrastructure-engineering.terraform.upgrading-terraform-core-versions
name: upgrading-terraform-core-versions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, required-version, version-upgrade, terraform-upgrade, core-upgrade, tfenv, tenv, version-pinning, state-version, upgrade-guide, migration]
level: practitioner
status: docs-checked
description: "Upgrade Terraform core safely: pin with required_version, read each upgrade guide, remember downgrades are not guaranteed, and migrate to OpenTofu."
sources: ["https://developer.hashicorp.com/terraform/language/upgrade-guides", "https://developer.hashicorp.com/terraform/language/terraform", "https://developer.hashicorp.com/terraform/language/v1-compatibility-promises", "https://opentofu.org/docs/intro/migration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Terraform core versions and required_version

**Goal:** move a repo from one Terraform version to another without a surprise
state-format change that locks out everyone on the old binary.

## 1. Pin it
```hcl
terraform {
  required_version = "~> 1.9.0"   # any 1.9.x; CI and devs match
}
```
- `required_version` limits which Terraform CLI may run the configuration; Terraform
  errors and exits otherwise. It must be satisfied by the root and by every module's
  constraint, and it does not apply to provider versions.
- Modules declare the **minimum** they need; root modules pin tighter.
- A `.terraform-version` file read by tfenv selects the version automatically
  (`tfenv install` with no argument installs it).
- In CI, install the same version the repo pins; never track `latest` unpinned.

## 2. Downgrades are not guaranteed
The v1.x compatibility promise: upgrading from any 1.x to any later 1.x should work with
no special steps. Downgrading is not guaranteed: later releases may add new storage
formats for state snapshots, and using a newer language feature makes the configuration
incompatible with releases before it. So:
1. Upgrade everyone (CI and humans) in the same window; the first newer apply may lock out older binaries.
2. Back up state before the first apply with the new version (for example `terraform state pull > backup.tfstate`).
3. Rolling back after a newer version wrote state may not be possible; test the upgrade on a copy first.

## 3. Procedure
```bash
git switch -c upgrade-tf
terraform init -upgrade                 # also upgrades providers within constraints: review the lock diff
terraform validate
terraform plan -out=tfplan              # expect: No changes. Anything else is the upgrade's doing
```
- Read the upgrade guide for every minor release between old and new (the Upgrading to
  Terraform vX.Y pages; use the version selector).
- Bump `required_version`, commit `.terraform.lock.hcl`, open a PR whose plan shows no
  changes, merge, then announce.
- After upgrading, run `terraform fmt`: the docs say canonical formatting may change in
  minor ways between versions.
- Across large gaps, upgrade one minor at a time, reading each guide.

## 4. OpenTofu
OpenTofu aims to maintain compatibility with Terraform configurations. Its migration
guide: back up state and code, install OpenTofu, initialize and verify the configuration,
then test with a small change. Configurations connected by `terraform_remote_state` need
extra care (see its guide on interdependent configurations).
## Gotchas
- `terraform init -upgrade` also upgrades providers; to upgrade core only, run plain
  `terraform init`, and upgrade providers in a separate PR.
- HCP Terraform workspaces have their own Terraform version setting; keep it compatible
  with the repo's `required_version`.
- A module in the tree may require a Terraform version your CLI does not meet; `init`
  fails naming the constraint.

## Verify
- [ ] `terraform version` matches the repo pin and CI on every machine.
- [ ] Post-upgrade `terraform plan` on every root module shows no changes.
- [ ] A state backup from before the upgrade exists and its location is in the PR.

## Checked
Date: 2026-10-28.
Confirmed in the terraform block reference: `required_version` semantics, errors when unmet, all module constraints apply, provider versions excluded. Confirmed in the v1.x compatibility promises: upgrade and downgrade wording, new state storage formats, new language features break older releases, `init -upgrade` is a protected flag. Confirmed in the fmt command page: formatting may change between versions. Confirmed in the tfenv README: `.terraform-version`. Confirmed in the OpenTofu migration page: steps and `terraform_remote_state` note.
Removed as unconfirmed: the 0.12/0.13/0.14/0.15 milestone table, quoted state-version error text, `state push -force` rollback advice, per-minor feature map, tenv commands, Terragrunt and `tfe_workspace` notes, OpenTofu version-parity and feature lists.
Method: documentation only; no commands were run.
