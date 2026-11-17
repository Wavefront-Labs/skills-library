---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.dependency-lock-files-and-provider-upgrade-testing
name: dependency-lock-files-and-provider-upgrade-testing
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, dependency-updates, lock-file, dependency-lock, provider-upgrade, upgrade-testing, terraform-lock-hcl]
level: practitioner
status: docs-checked
description: "Commit .terraform.lock.hcl with multi-platform hashes, pin Ansible collections, and test provider or collection upgrades with no-change plans before merging."
sources: ["https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://developer.hashicorp.com/terraform/cli/commands/providers/lock", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/language/modules/configuration", "https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency lock files and provider upgrade testing

## Terraform lock file
`terraform init` writes the selected provider versions and checksums to the dependency lock file. **Commit it** to version control so later `init` runs select exactly the same provider versions. The lock file lives in the root module's working directory.

Checksums are per platform. If a team runs Terraform on several platforms, pre-populate hashes for all of them (repeat `-platform=OS_ARCH`):
```bash
terraform providers lock \
  -platform=linux_amd64 -platform=windows_amd64 -platform=darwin_amd64
```
Upgrade deliberately: `terraform init -upgrade` ignores the lock selections and takes the newest versions allowed by the constraints (it also updates modules). Commit the lock change in its own PR.

CI guard: `terraform init -lockfile=readonly` suppresses lock file changes and verifies checksums against what is recorded; it conflicts with `-upgrade`.

## Ansible
Pin collections to exact versions in a requirements file (`collections:` list with `name` and `version`):
```yaml
# requirements.yml
collections:
  - name: amazon.aws
    version: "8.2.1"
```
Version ranges such as `">=1.2.0"` are allowed in the file, so use exact versions when you want a lock.

## Testing an upgrade
1. Branch; bump one provider or collection (or a coherent group).
2. Read the project's changelog and upgrade guide for breaking changes.
3. Terraform: `terraform plan` in every environment; the expected result is **no changes**. Any diff caused only by the upgrade needs explanation. `terraform plan -detailed-exitcode` returns 0 for no changes and 2 for changes present; fail CI on 2 for upgrade PRs.
4. Apply to a non-prod environment, then prod.

## Gotchas
- Back up state before applying an upgrade (`terraform state pull` writes the state to stdout).
- Pin `required_version` to constrain the Terraform CLI itself (it does not constrain providers).
- The lock file tracks only providers. Pin modules with an exact `version` constraint (registry) or a `?ref=` tag or commit (git source).

## Verify
- [ ] The lock file is tracked in version control in every root module.
- [ ] Upgrade PR shows "No changes" plans for all environments.

## Checked
2026-11-01. Confirmed in the Terraform dependency lock, `providers lock`, `init`, `plan` and module configuration pages and the Ansible collections installing page: commit-the-lock-file advice, per-platform checksums and `-platform=OS_ARCH`, `-upgrade`, `-lockfile=readonly` behaviour, `-detailed-exitcode` codes 0 and 2, `required_version` scope, providers-only lock, `?ref=` sources, requirements file `name`/`version` and ranges. Removed: darwin_arm64 example, "no lock file in ansible-galaxy", execution environment and pip-compile advice, Molecule and `--check` steps, the claims about state rewrites and state format versions, and the specific CHANGELOG/Version 6 guide references.
Method: documentation only; no commands were run.
