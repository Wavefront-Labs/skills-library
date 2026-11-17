---
id: computing-software.cloud-infrastructure-engineering.terraform.providers-lock-platform-for-multi-os-lockfiles
name: providers-lock-platform-for-multi-os-lockfiles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, providers-lock, lock-platform, multi-platform-lockfile, lock-file, dependency-lock, terraform-lock-hcl, darwin-arm64, linux-amd64, checksum]
level: practitioner
status: verified
description: "Make .terraform.lock.hcl work for macOS laptops and Linux CI at once with terraform providers lock -platform, so init never fails with a missing-checksum error."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/providers/lock", "https://developer.hashicorp.com/terraform/language/files/dependency-lock#new-provider-package-checksums"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform providers lock -platform` for multi-OS lock files

**Goal:** one committed lock file that satisfies every OS/arch your team and
pipelines run on.

## 1. The problem
`terraform init` records an `h1:` checksum (hash of the unpacked package) only for the platform it ran on. When the provider comes
from the origin registry it also records `zh:` zip checksums for every platform (13 `zh:` lines and one `h1:` after `init` for
`hashicorp/null` on 1.17.0), which already lets other platforms verify a registry download. The lock file is incomplete mainly when
providers come from a mirror (a mirror yields only `h1:`; a filesystem-mirror `init` wrote one `h1:` and no `zh:`), or when you
want `h1:` for every platform to avoid lock-file diffs when other platforms run `init`.

## 2. The fix
```bash
terraform providers lock \
  -platform=linux_amd64 \
  -platform=linux_arm64 \
  -platform=darwin_amd64 \
  -platform=darwin_arm64 \
  -platform=windows_amd64
git add .terraform.lock.hcl && git commit -m "lock providers for all platforms"
```
- Downloads each provider package for each platform (no install), computes `h1:`
  hashes, and merges them into the existing lock entries. Version selections are
  unchanged. (Listing the five platforms above gave five `h1:` lines and the same 13 `zh:`; adding `freebsd_amd64` and
  `windows_386` gave seven.)
- Run it after **every** provider version bump (`init -upgrade`), otherwise the new
  version has one platform again.
- Platform names: `<os>_<arch>` — `linux_amd64`, `linux_arm64`, `darwin_amd64`,
  `darwin_arm64`, `windows_amd64`, `windows_386`, `freebsd_amd64`.

## 3. Options
- `-fs-mirror=DIR` / `-net-mirror=URL` — hash packages from a mirror instead of the
  registry (air-gapped). Mirrors give `h1:` only (a run with `-fs-mirror` over a `providers mirror` directory gave two `h1:` for two platforms and
  no `zh:`); the registry also supplies `zh:` (zip hashes) for every platform, which is why registry-sourced lock entries list
  many `zh:` lines.
- `providers lock hashicorp/null` — restrict to named providers. Put flags first: `providers lock hashicorp/null -platform=linux_amd64`
  fails with `Invalid provider type "-platform=linux_amd64"`, and naming a provider the configuration does not require fails with
  `The provider ... is not required by the current configuration`.
- `-enable-plugin-cache` — reuse the plugin cache during the download (`providers lock -help` on 1.17.0: speeds up locking, but the
  providers are not loaded from an authoritative source).

## 4. Automate it
Add a CI check so nobody commits a single-platform lock:
```bash
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64
git diff --exit-code .terraform.lock.hcl || { echo "lock file missing platforms"; exit 1; }
```
Renovate/Dependabot bump commits do not run this; add the command to the
post-upgrade hook or a follow-up job.

## Gotchas
- The command needs network access to the registry for every platform listed;
  without `-enable-plugin-cache` it does not read your plugin cache for hashes.
- OpenTofu: the lock file format is the same, but `tofu init` rewrote a Terraform-generated lock into a
  `registry.opentofu.org/...` entry with different hashes (OpenTofu 1.13.2) — do not share a lock
  file between `terraform` and `tofu` runs of the same directory.
- `h1:` covers the unpacked content; `zh:` covers the zip. Either is enough to
  verify; both present is normal.
- `windows_386` and 32-bit Linux platforms are rarely needed; every extra platform adds a download and another `h1:` line.

## Verify
- [ ] `grep -c "h1:" .terraform.lock.hcl` shows one `h1:` per provider per platform you listed.
- [ ] `terraform init` on Linux CI prints "Using previously-installed" and does not modify the lock file (`git diff --exit-code`).

## Checked
- Terraform 1.17.0 on `hashicorp/null`: `init` lock had 1 `h1:` + 13 `zh:`; `providers lock` with five `-platform` flags gave five `h1:` and kept 13 `zh:`, and a re-run with the same platforms left `git diff --exit-code` clean (the CI check pattern, no-diff path); extra platforms raised it to seven; `providers lock -help` text for each option; flag-after-argument error and non-required provider error reproduced; `-enable-plugin-cache` ran; `-fs-mirror` over a `providers mirror` tree gave `h1:` only; `tofu init` replaced a Terraform lock entry with a `registry.opentofu.org` entry.
- The Linux-CI failure message quoted in the old text could not be reproduced (no Linux host) and was removed; the text now describes what the lock file contents show. The Renovate/Dependabot hook advice is procedural.
