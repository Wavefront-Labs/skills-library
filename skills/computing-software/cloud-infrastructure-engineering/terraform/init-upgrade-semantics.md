---
id: computing-software.cloud-infrastructure-engineering.terraform.init-upgrade-semantics
name: init-upgrade-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, init-upgrade, upgrade-flag, terraform-init, lock-file, provider-upgrade, module-upgrade, version-constraints, get-update]
level: intro
status: verified
description: "What terraform init -upgrade actually changes: provider selection within constraints, module re-download, lock file rewrite, and how to keep it out of CI."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#plugin-installation", "https://developer.hashicorp.com/terraform/language/files/dependency-lock#dependency-installation-behavior", "https://developer.hashicorp.com/terraform/cli/commands/get"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform init -upgrade` semantics

**Goal:** upgrade providers and modules deliberately, in a reviewable commit, and
never by accident in a pipeline.

## 1. What plain `init` does
- Providers: if `.terraform.lock.hcl` has an entry, install **exactly** that version
  and verify the checksum. If no entry, select the newest version matching
  `required_providers` constraints and write it to the lock file.
- Modules: if `.terraform/modules/modules.json` already has the module, reuse it
  (even for `git` sources with a moving `ref`). Otherwise download.

## 2. What `-upgrade` adds
```bash
terraform init -upgrade
```
- Providers: ignore the locked version; pick the **newest** version satisfying the
  constraints and rewrite the lock entry (version + hashes for this platform only).
  Versions outside the constraint are never chosen — a `~> 5.0` constraint stays on
  5.x.
- Modules: re-download every module source. For registry modules this re-resolves
  `version` constraints; for `git` sources it re-fetches the ref; for local paths
  nothing changes.
- Equivalent to `terraform get -update` plus provider upgrade.

## 3. The upgrade workflow
```bash
# 1. widen or bump the constraint in versions.tf
#    aws = { source = "hashicorp/aws", version = "~> 5.60" }
terraform init -upgrade
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64   # re-add platforms
terraform plan                                                           # check for provider-induced diffs
git add versions.tf .terraform.lock.hcl && git commit -m "aws provider 5.60"
```
Review the lock-file diff: version lines and hash lines should change only for the
providers you intended.

## 4. Keep it out of CI
CI should run plain `terraform init -input=false`. With `-upgrade`, every pipeline
run could silently pick a new patch release, the lock file diverges from the
commit, and a plan may differ from what the developer saw. Grep pipeline
definitions for `-upgrade` and remove it.

## Gotchas
- `-upgrade` does not touch `required_version` (core) — only providers/modules.
- With a constraint like `>= 5.0` (no upper bound) `-upgrade` can jump a major
  version; prefer `~>` (ran: `~> 3.5` moved `random` from 3.5.1 to 3.9.1 and stayed on 3.x).
- Lock entries for providers no longer referenced are removed on `init`; not an
  error, just a diff (ran: dropping `null` from `required_providers` left one lock entry after a plain `init`).
- `init -upgrade` for a **git module with no ref** pulls the default branch head;
  the change is invisible in the config — pin a `ref=` tag.
- OpenTofu: `tofu init -upgrade` takes the same flag (ran on 1.13.2) and resolves providers from the OpenTofu registry, so confirm a brand-new provider release is available there before pinning to it.

## Verify
- [ ] After `init -upgrade`, `git diff .terraform.lock.hcl` shows only the intended providers.
- [ ] `terraform plan` after the upgrade shows no unexpected changes (provider default changes are common on major bumps).
- [ ] No `init -upgrade` in CI config.

## Checked
- Terraform 1.17.0 with `random` and `null`: a lock at `= 3.5.1` survived a plain `init` after the constraint was loosened to `~> 3.5` (`Reusing version 3.5.1`); `init -upgrade` installed 3.9.1 and rewrote version and constraints; an unreferenced provider vanished from the lock; `providers lock -platform=linux_amd64 -platform=darwin_arm64` added hashes (1 to 3 `h1:` entries); a local git module source stayed at its first commit after a plain `init` and was refetched by `init -upgrade`.
- Also ran: `init -upgrade` still enforces `required_version` (`Unsupported Terraform Core version` for `>= 99.0`) and writes nothing about it to the lock file. The `aws ~> 5.60` lines are an example constraint only, not a claim about AWS provider versions.
- A registry module (`hashicorp/dir/template`, versions 1.0.1 and 1.0.2): with the constraint loosened from `1.0.1` to `>= 1.0.1` a plain `init` kept 1.0.1 (no download, `modules.json` still 1.0.1) and `init -upgrade` downloaded 1.0.2.
