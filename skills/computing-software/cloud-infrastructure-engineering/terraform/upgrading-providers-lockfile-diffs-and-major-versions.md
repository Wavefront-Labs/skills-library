---
id: computing-software.cloud-infrastructure-engineering.terraform.upgrading-providers-lockfile-diffs-and-major-versions
name: upgrading-providers-lockfile-diffs-and-major-versions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-upgrade-lockfile, upgrade-diff, major-version-upgrade, deprecation-warnings, init-upgrade, lock-file]
level: advanced
status: docs-checked
description: "Upgrade providers deliberately: init -upgrade, review .terraform.lock.hcl diffs, read upgrade guides, clear deprecation warnings, and roll major versions env by env."
sources: ["https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://developer.hashicorp.com/terraform/cli/commands/providers/lock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider upgrades: lock file diffs and majors

## Minor/patch upgrade
```bash
terraform init -upgrade
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64
git diff .terraform.lock.hcl
terraform plan
```
- Without `-upgrade`, a provider already recorded in the lock file is always re-selected at that version, even if a newer one exists. `-upgrade` ignores the recorded selections and picks the newest version matching the constraints. `-upgrade` applies to modules as well as plugins, so review module changes too.
- A new provider version normally changes `version` in the lock block and replaces most `hashes` values; `constraints` changes only if you changed the version constraint.
- The lock file only holds checksums for the platform where `init` ran (plus any the registry signed). Pre-populate other platforms with `terraform providers lock -platform=...` so other OSes and CI do not hit checksum errors or keep adding `h1:` hashes.

Lock diff review:
```diff
 provider "registry.terraform.io/hashicorp/aws" {
-  version     = "5.70.0"
+  version     = "5.82.2"
   constraints = "~> 5.70"
   hashes = [
```
- Exactly the providers you meant changed; versions within constraints.
- Hashes cover every platform CI and devs use.
- Read the provider changelog between the versions for behaviour changes and new defaults.

## Plan review
A provider upgrade PR should ideally plan with no changes in every environment. Any diff means new defaults or normalisation changes; understand each before merging.

## Major upgrade
1. Read the provider's upgrade guide (on the provider's registry docs page).
2. Fix deprecation warnings on the current major first, as deprecations usually signal removals in the next major; `terraform validate` and `plan` print them.
3. Raise the constraint, `terraform init -upgrade`, fix errors.
4. Roll out dev, staging, prod in turn; each env's plan must be clean or every change explained.
5. Widen `version` ranges in reusable modules only after they are tested on both majors.

## Rollback
Revert the lock file and constraint, then `terraform init`. If an apply already ran with the new provider, state may have been written by a newer provider version and an older provider may refuse it; then roll forward instead.

## Gotchas
- Running `-upgrade` casually in CI makes builds non-reproducible; use it only in upgrade PRs and commit the lock file.

## Verify
- [ ] Lock file hashes cover all team/CI platforms.
- [ ] No new deprecation warnings after the upgrade; plans clean in all envs.

## Checked

Method: docs-checked 2026-11-09 against the dependency lock file page (version upgrade, checksum and `providers lock` sections), the `init` reference (-upgrade for modules and plugins) and the `providers lock` reference (downloaded, converted to text and read). Dropped unconfirmed claims: the AWS v6 specifics and registry upgrade-guide source (not readable), the jq command for collecting warnings, and the exact "managed by newer provider version" error text.
