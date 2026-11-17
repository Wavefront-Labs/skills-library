---
id: computing-software.cloud-infrastructure-engineering.google-cloud.terraform-google-provider-version-upgrades
name: terraform-google-provider-version-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, infrastructure-as-code, terraform-provider-versions, provider-upgrade, google-beta, lock-file]
level: advanced
status: draft
description: "Upgrade the Terraform google and google-beta providers safely: version constraints, the lock file, reading major-version upgrade guides, default labels changes, and plan-diff review."
sources: ["https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/version_6_upgrade", "https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://cloud.google.com/docs/terraform/best-practices/version-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terraform Google provider version upgrades

## 1. Constraints and lock file
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    google      = { source = "hashicorp/google",      version = "~> 6.10" }
    google-beta = { source = "hashicorp/google-beta", version = "~> 6.10" }
  }
}
```
Commit `.terraform.lock.hcl`. Upgrade deliberately:
```bash
terraform init -upgrade
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64
```
Keep `google` and `google-beta` on the same version.

## 2. Minor versions
Weekly releases; usually safe. Read the CHANGELOG for "BREAKING" in minor releases of beta resources and
for new default values that show as diffs.

## 3. Major versions (e.g. 5 → 6)
1. Read the **version N upgrade guide** (removed fields, renamed resources, changed defaults).
2. Upgrade to the latest of the old major first; fix all deprecation warnings.
3. Bump the constraint, `init -upgrade`, run `plan` for **every** root, review diffs line by line.
Past examples: v5 introduced `labels`/`effective_labels`/`terraform_labels` and provider `default_labels`;
v6 made `deletion_protection` defaults stricter for several resources and removed long-deprecated fields.

## 4. Modules
Shared modules should declare minimum versions (`>= 5.0, < 7.0`), not pin exact ones, so roots control the version.

## Gotchas
- A plan that wants to replace stateful resources after upgrade is a stop sign: look for changed defaults, use `lifecycle.ignore_changes` only temporarily.
- State upgrades are one-way: after applying with a new major, older providers may not read the state. Back up state (GCS versioning) first.
- Third-party modules (terraform-google-modules) lag provider majors; check their supported range.

## Verify
- [ ] All roots plan with zero unexpected changes on the new version; CI uses the lock file (`init -lockfile=readonly`).
