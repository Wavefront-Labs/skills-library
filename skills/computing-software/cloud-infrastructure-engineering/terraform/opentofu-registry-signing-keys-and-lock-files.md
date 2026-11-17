---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-registry-signing-keys-and-lock-files
name: opentofu-registry-signing-keys-and-lock-files
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tofu-lockfile, provider-gpg-keys, tofu, dependency-lock, opentofu-migration]
level: practitioner
status: docs-checked
description: "Handle provider signing and lock files when moving between Terraform and OpenTofu: registry.opentofu.org addresses, GPG key verification, and regenerating hashes for both tools."
sources: ["https://opentofu.org/docs/language/files/dependency-lock/", "https://opentofu.org/docs/internals/provider-registry-protocol/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTofu registry, signing keys and lock files

## Hostnames differ
OpenTofu's lock file (`.terraform.lock.hcl`) records the full provider address, and the OpenTofu docs show entries such as `provider "registry.opentofu.org/hashicorp/azurerm"`. Terraform's default registry host is `registry.terraform.io`, so a lock file written by one tool lists different provider addresses from the other. After switching tools, expect `tofu init` to add `registry.opentofu.org/...` entries and review the lock diff before committing.

## Practical approach
- Pick one tool per root module and commit its lock file.
- Hashes: `tofu init` records checksums only for the platform it ran on (plus any the registry signed), which leaves the lock unusable on other platforms when installing from a mirror. Pre-populate them:
```bash
tofu providers lock -platform=linux_arm64 -platform=linux_amd64 -platform=darwin_amd64 -platform=windows_amd64
```
  This downloads and verifies the official packages and records both `zh:` and `h1:` checksums for each platform.
- `tofu init -upgrade` picks the newest version allowed by the constraints, and the lock diff changes `version` and `hashes` for the affected providers.

## Signing keys
The provider registry protocol (package response) carries `shasums_url`, `shasums_signature_url` and a `signing_keys` object. `gpg_public_keys` must list at least one key (with `key_id` and `ascii_armor`) that produced the detached signature over the SHA256SUMS document. Clients verify the signature with those keys. The key lists differ per registry, so verify behaviour on your own providers rather than assuming the two registries share keys.

## Pinning to the original registry (if required)
```hcl
required_providers {
  aws = { source = "registry.terraform.io/hashicorp/aws", version = "~> 5.70" }
}
```
A fully qualified `source` selects that registry host; check the registry's terms of use for non-Terraform clients.

## Verify
- [ ] Lock file lists the platforms your CI and developers use (`tofu providers lock`).
- [ ] The regenerated lock is committed and `tofu init` passes in CI.

## Checked

Method: docs-checked 2026-11-09 against the OpenTofu dependency lock file page and the provider registry protocol page (downloaded, converted to text and read). Dropped unconfirmed claims: failure with `-lockfile=readonly`, automatic state provider-address mapping, the `opentofu/registry` GitHub key repository and the `Signing key not found` warning, and the Terraform-side key statements; removed the unread GitHub source.
