---
id: computing-software.cloud-infrastructure-engineering.terraform.switching-to-opentofu-init-registry-and-compatibility
name: switching-to-opentofu-init-registry-and-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [opentofu, terraform, tofu-init, tofu-registry, tofu-compatibility, migrate-back, tofu-extension, dot-tofu-files, migration]
level: advanced
status: docs-checked
description: "Switch a Terraform codebase to OpenTofu: tofu init against registry.opentofu.org, version compatibility, .tofu override files, and how to migrate back."
sources: ["https://opentofu.org/docs/intro/migration/", "https://opentofu.org/docs/language/files/", "https://opentofu.org/docs/cli/commands/test/", "https://opentofu.org/docs/language/files/dependency-lock/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switching to OpenTofu (and back)

## Compatibility baseline
OpenTofu aims to maintain compatibility with Terraform configurations; most code works without modification, and the project publishes a migration guide whose overview steps are: back up state and code, install OpenTofu, initialise and verify the configuration, then test with a small change. The migration is described as safe and reversible. Follow the guide for your Terraform version, and see its note on migrating interdependent configurations that share data through `terraform_remote_state`.

## Steps
1. Make sure state is current with your existing Terraform version (`terraform apply`) and take a backup (`terraform state pull > pre-tofu.tfstate`).
2. Install OpenTofu and pin the version.
3. `tofu init`. Provider addresses in the lock file use `registry.opentofu.org/...`; the lock file gains OpenTofu entries and hashes, so commit it. Pre-populate other platforms with `tofu providers lock -platform=...`.
4. `tofu plan` should show no changes; investigate anything else before applying.
5. Apply a trivial change to prove the write path, then switch CI to `tofu`.

## .tofu files
OpenTofu loads `.tf` and `.tofu` files (and `.tf.json` / `.tofu.json`). If `foo.tf` and `foo.tofu` exist in the same directory, OpenTofu loads only `foo.tofu` and ignores `foo.tf`; the docs describe this as useful for module authors who want to support both tools. Terraform does not read `.tofu` files, so a `.tofu` file carries OpenTofu-only configuration beside a Terraform-compatible `.tf` file.
```
versions.tf      # Terraform-compatible version
versions.tofu    # OpenTofu-only variant (loaded instead of versions.tf by tofu)
```
Tests follow the same rule: `tofu test` runs `*.tftest.hcl`, `*.tftest.json`, `*.tofutest.hcl` and `*.tofutest.json`, and a `.tofutest.hcl` file takes precedence over a `.tftest.hcl` of the same base name.

## Version constraints
`required_version` is evaluated against OpenTofu's own version numbers, which differ from Terraform's. Check constraints written for Terraform and put OpenTofu-specific ones in `.tofu` files.

## Migrating back
Remove OpenTofu-only syntax and data first, run `terraform init` (the lock file will need Terraform-registry entries) and confirm `terraform plan` shows no changes. Check the specific version's migration guide for state compatibility before relying on this.

## Verify
- [ ] `tofu plan -detailed-exitcode` exits 0 in every workspace after switching.
- [ ] The lock file in CI covers all platforms in use.

## Checked

Method: docs-checked 2026-11-09 against the OpenTofu migration overview, files and directories page (extension precedence), `tofu test` page (test file precedence) and dependency lock page (downloaded, converted to text and read). The per-version migration guides did not return readable content. Dropped unconfirmed claims: the Terraform 1.5 fork baseline and version list, listed incompatible features, the `.opentofu-version`/tenv/mise pinning tools, decrypt-first migrate-back steps, HCP Terraform licensing remarks, and the provider-registry-protocol source.
