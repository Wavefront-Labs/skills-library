---
id: computing-software.cloud-infrastructure-engineering.terraform.lock-file-hashes-and-checksum-mismatch-errors
name: lock-file-hashes-and-checksum-mismatch-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, h1-hash, zh-hash, checksum-mismatch, lock-file, dependency-lock, provider-verification, registry-mirror, supply-chain]
level: practitioner
status: verified
description: "Read the h1: and zh: lines in .terraform.lock.hcl, diagnose 'does not match any of the checksums' errors, and fix them without blindly deleting the lock file."
sources: ["https://developer.hashicorp.com/terraform/language/files/dependency-lock#checksum-verification", "https://developer.hashicorp.com/terraform/cli/commands/providers/lock", "https://developer.hashicorp.com/terraform/internals/provider-registry-protocol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock file hashes and checksum-mismatch errors

**Goal:** understand what the hashes in `.terraform.lock.hcl` prove, so a
mismatch is handled as a supply-chain signal, not an annoyance.

## 1. Anatomy
```hcl
provider "registry.terraform.io/hashicorp/null" {
  version     = "3.3.2"
  constraints = "~> 3.2"
  hashes = [
    "h1:7rn0+p+fbrHfJxNVgTnlKp6C3yu0jENMXffz9Xb9XjQ=",   # hash of the UNPACKED package contents, one per platform seen
    "zh:10ec43b8b7b18d5639238c7fb9e111f6a4b038523dd66c7a426bf27b25fa4c08",   # SHA-256 of a ZIP, from the registry's SHA256SUMS
    "zh:...",
  ]
}
```
Real lock file written by `terraform init` 1.17.0 on windows_amd64: **one** `h1:` (the platform it ran on) and **13** `zh:` lines (the registry's zips for
every platform).
- `h1:` (hash scheme 1) is computed by Terraform from the extracted directory; it is
  platform-specific because the binary differs per platform.
- `zh:` ("zip hash") is the registry's SHA256SUMS entry, which Terraform verifies
  against the provider author's GPG signature. Registry installs add all platforms'
  `zh:` at once, so a registry-sourced lock already covers CI on Linux via `zh:`.
- Mirrors (`filesystem_mirror`, `network_mirror`) can only produce `h1:` — hence
  `providers lock -platform` for mirror users.

## 2. The error
```
Error: Failed to install provider
Error while installing hashicorp/null v3.3.2: the current package for
registry.terraform.io/hashicorp/null 3.3.2 doesn't match any of the checksums
previously recorded in the dependency lock file; for more information:
https://developer.hashicorp.com/terraform/language/files/dependency-lock#checksum-verification
```
(Reproduced by replacing every hash in a lock file with a bogus value and running `init`.)
Causes, in order of likelihood:
1. Lock file was generated from a different **source** (registry vs mirror, or
   OpenTofu registry vs HashiCorp registry) — the package is byte-different.
2. Plugin cache (`TF_PLUGIN_CACHE_DIR`) holds a stale/corrupt copy from a previous
   build of the same version (pre-release re-tag or a mirror that re-zipped).
3. A proxy/mirror is serving a modified package — **treat as compromise** until
   proven otherwise.
4. Someone hand-edited the lock file.

## 3. Fix
```bash
# confirm what the registry says
curl -s https://registry.terraform.io/v1/providers/hashicorp/null/3.3.2/download/linux/amd64 | jq .shasum
# compare with your package
sha256sum terraform-provider-null_3.3.2_linux_amd64.zip
# if the registry hash matches and only the lock file is off: regenerate the entry
rm .terraform.lock.hcl   # ONLY after confirming the registry hash
terraform init
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64
```
If a cache is the culprit: delete that provider's directory from
`$TF_PLUGIN_CACHE_DIR` and re-run `init`. By default Terraform uses a cached package only if the lock file already has an
entry confirming it; `plugin_cache_may_break_dependency_lock_file = true` (or `TF_PLUGIN_CACHE_MAY_BREAK_DEPENDENCY_LOCK_FILE`)
is the CLI-config opt-out, documented for exceptional situations only, so leave it unset.

## 4. Policy
- Lock file is committed; CI runs plain `init` so any mismatch fails the build.
- OpenTofu and Terraform teams sharing a repo: do not assume the lock file is shared. In a test, `tofu init` (1.13.2) on a
  Terraform-generated lock file for `hashicorp/null` 3.3.2 produced a lock whose only entry is `registry.opentofu.org/hashicorp/null`
  (15 `h1:` and 15 `zh:`, none equal to Terraform's `h1:7rn0+...`), because the provider address and registry differ.
  Standardise on one tool per repo, or keep separate lock files and run `providers lock -platform` with that tool.

## Gotchas
- `terraform init` **appends** hashes it learns; it never removes a valid hash.
  A lock entry with hashes for a version that later gets "re-released" (rare but it
  has happened for community providers) is exactly the mismatch case — verify
  against the registry before trusting the new package.
- Deleting the lock file also drops version pins; your next `init` may select
  newer versions — review `versions.tf` constraints first.

## Verify
- [ ] After the fix, `terraform init` prints "Using previously-installed ..." with no lock file diff.
- [ ] The `zh:` for your platform in the lock file equals the registry `shasum` for that version.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2, `hashicorp/null` 3.3.2: lock file anatomy (1 `h1`, 13 `zh` after `init`); bogus-hash lock file gave the quoted error; the registry download API `shasum` for windows/amd64 and linux/amd64 equalled a `zh:` line in the lock, and `sha256sum` of the mirrored windows zip equalled the same value (so `zh` is the zip SHA-256); a filesystem-mirror install produced only an `h1:` (1 `h1`, 0 `zh`, package "unauthenticated"); `tofu init` on the Terraform lock produced a `registry.opentofu.org` entry with different hashes.
- Docs fetched: dependency-lock page (`zh:` is a legacy zip hash from the registry protocol; Terraform opportunistically adds `h1:`), CLI config page (`plugin_cache_may_break_dependency_lock_file`, env var, default behaviour). The "Terraform 1.4+" label could not be confirmed in the changelog and was removed.
- The policy list and the suggestion to delete the lock file only after verifying the registry hash are procedure, not behavioural claims; the unverified GPG-failure bullet was removed.
