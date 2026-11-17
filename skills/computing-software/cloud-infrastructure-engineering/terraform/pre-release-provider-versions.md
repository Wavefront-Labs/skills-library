---
id: computing-software.cloud-infrastructure-engineering.terraform.pre-release-provider-versions
name: pre-release-provider-versions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, prerelease-provider, provider-version, version-constraints, provider-upgrade]
level: practitioner
status: docs-checked
description: "Test beta and RC provider releases safely: exact-version constraints required for pre-releases, isolating them to a sandbox root, lock file handling, and rolling back."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/version-constraints#version-constraint-behavior", "https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-release provider versions

## Constraint rules
A pre-release version has a suffix introduced by a dash (`6.0.0-beta2`, `5.0.0-rc2`).
Terraform selects one only when the constraint is the exact version, with `=` or no
operator. It does not match pre-releases on `>`, `>=`, `<`, `<=` or `~>`:
```hcl
required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "6.0.0-beta2"       # exact; ranges never match pre-releases
  }
}
```
So `~> 6.0` will not pick `6.0.0-beta2`. `=` cannot be combined with other conditions.

## Safe testing workflow
1. Use a separate sandbox root module (or branch) with the exact pre-release
   constraint; commit nothing to shared roots.
2. If the lock file already records another version of that provider, run
   `terraform init -upgrade` so Terraform disregards the recorded selection; otherwise a
   recorded selection is always re-selected.
3. Run plan against a test environment or separate state, not production state.
4. Read the provider's upgrade guide items one by one and report issues upstream with
   versions.

## Modules
Terraform proceeds only if the constraints of the root module and all child modules are
met. If a shared module declares `>= 5.30, < 6.0`, an exact pre-release such as
`6.0.0-beta2` cannot satisfy it (ranges do not match pre-releases), so test with a local
copy of the module or relax its constraint on a branch. Shared modules should normally
constrain only a minimum with `>=`; root modules should use `~>` for both bounds.

## Rolling back
Take a backup of state before testing and never apply a pre-release against production
state. Terraform refreshes a resource whose schema version changes regardless of the plan
result, and the plan docs advise against `-refresh=false` when upgrading providers; keep
the backup so you can restore it if you applied a pre-release by mistake.

## Lock file
The lock file (`.terraform.lock.hcl`) records for each provider the exact `version`,
the `constraints` considered, and `hashes`. To revert, change the constraint back and
run `terraform init -upgrade`, which disregards the existing selection and picks the
newest version matching the constraint. Review the lock file diff in code review.

## Checked
Date: 2026-11-07
Read in full: "Version constraints" (incl. Specify a pre-release version, Best practices) and "Dependency Lock File" (all sections).
Confirmed: exact-version rule and the operators that never match pre-releases, `=` cannot be combined, all module constraints must be met, `>=` for shared modules and `~>` for roots, lock file contents (version, constraints, hashes), `init -upgrade` overriding recorded selections, review of lock diffs.
Removed (not on the pages): the "Resource instance managed by newer provider version" error text, the claim that pre-releases upgrade the state schema version (replaced by the schema-version refresh note on the `terraform plan` page, read in full), "pull and push a copy of state", and the grep Verify step. The `-upgrade` step is now conditional on an existing lock entry.
Method: documentation only; no commands were run.
