---
id: computing-software.cloud-infrastructure-engineering.terraform.renovate-and-dependabot-terraform-version-bumps
name: renovate-and-dependabot-terraform-version-bumps
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, renovate, dependabot-terraform, version-bump-automation, dependency-bumps, lock-file, required-version]
level: practitioner
status: docs-checked
description: "Automate Terraform core, provider and module version bumps with Renovate or Dependabot (lock file maintenance, grouping) and review those PRs safely."
sources: ["https://docs.renovatebot.com/modules/manager/terraform/", "https://docs.renovatebot.com/modules/manager/terraform-version/", "https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renovate / Dependabot for Terraform

## Renovate
The terraform manager updates modules (git tags, GitHub tags, Terraform registry),
providers and the `required_providers` block (needs Terraform 0.13 or later),
`required_version`, `helm_release` versions, image references in `docker_*` and
`kubernetes_*` resources, and the `terraform_version` argument of tfe workspaces.
The separate terraform-version manager maintains `.terraform-version` files, with
versions taken from the official Terraform downloads page.
```json
{
  "extends": ["config:recommended"],
  "lockFileMaintenance": { "enabled": true },
  "packageRules": [
    { "matchManagers": ["terraform"], "matchDepTypes": ["provider"], "groupName": "terraform providers" },
    { "matchManagers": ["terraform"], "matchDepTypes": ["module"], "groupName": "terraform modules" },
    { "matchDatasources": ["terraform-provider"], "matchUpdateTypes": ["major"], "dependencyDashboardApproval": true }
  ]
}
```
- `lockFileMaintenance` is disabled by default; when on it deletes the lock file,
  lets the package manager regenerate it and opens a PR. Its default schedule is
  `before 4am on monday`.
- `dependencyDashboardApproval: true` makes Renovate wait for approval on the
  Dependency Dashboard before creating the branch/PR (works inside `packageRules`).
- By default Renovate uses `registry.terraform.io` for providers and modules
  without a registry definition; for OpenTofu set `registryUrls` to
  `https://registry.opentofu.org` for the `terraform-provider` and `terraform-module`
  datasources.
- Use `depType` values (`provider`, `required_provider`, `required_version`,
  `module`, `helm_release`, ...) to disable parts of the manager.
- Private registries need `hostRules` with `matchHost`.

## Dependabot
```yaml
version: 2
updates:
  - package-ecosystem: terraform
    directories: ["/live/*/*", "/modules/*"]
    schedule: { interval: weekly }
    groups:
      providers: { patterns: ["hashicorp/*"] }
```
Terraform is supported for version updates but not for Dependabot security
updates. `directories` supports globbing; `groups` take `patterns` and
`exclude-patterns`. Check how the lock file is handled in your repo and verify it
covers every platform your CI and developers use.

## Reviewing bump PRs
1. Lock diff: only intended providers changed; hashes for all platforms.
2. CI plan for **every** affected root shows `No changes` (or explained ones).
3. Read the changelog range (bot PR body links it); look for breaking changes and new defaults.
4. Majors: never auto-merge; follow the major-upgrade process.
5. Auto-merge only patch/minor provider bumps whose plans are clean, if your CI gates on plans.

## Core version bumps
Update `.terraform-version`/`required_version` and CI images together; state written
by a newer Terraform cannot be read by older versions.

## Verify
- [ ] Bot PRs trigger plans for all affected roots.
- [ ] Major provider bumps wait on dashboard approval.

## Checked
2026-11-09. Confirmed against the Renovate terraform and terraform-version manager readmes, the Renovate configuration options (`lockFileMaintenance` default and schedule, `dependencyDashboardApproval`, `hostRules`/`matchHost`) and the Dependabot options reference (Terraform version updates yes, security updates no; `directories` globbing; `groups` patterns).
Removed as unconfirmed: `.tool-versions` and setup-terraform handling, the `constraints.terraform` pin, the claim that Renovate runs `terraform providers lock`, the `before 6am` schedule, the `hashicorp/terraform` core grouping rule, and the statement that Dependabot is less flexible than Renovate for core files. The Dependabot source URL was updated to the current options reference.
Method: documentation only; no commands were run.
