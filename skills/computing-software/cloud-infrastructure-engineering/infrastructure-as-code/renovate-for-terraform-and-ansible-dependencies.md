---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.renovate-for-terraform-and-ansible-dependencies
name: renovate-for-terraform-and-ansible-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, dependency-updates, renovate, renovate-terraform, renovate-ansible, galaxy-requirements-updates, update-grouping]
level: practitioner
status: docs-checked
description: "What Renovate's terraform and ansible-galaxy managers update (modules, providers, lock file, requirements.yml) and how to target them with package rules."
sources: ["https://docs.renovatebot.com/modules/manager/terraform/", "https://docs.renovatebot.com/modules/manager/ansible-galaxy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renovate for Terraform and Ansible dependencies

## Terraform manager
- Checks `**/*.tf` and `**/*.tofu` by default.
- Datasources: `bitbucket-tags`, `docker`, `git-tags`, `github-releases`, `github-tags`, `helm`, `terraform-module`,
  `terraform-provider`.
- Modules come from Git tags, GitHub tags or the Terraform Registry (public or private). The `required_providers`
  block (Terraform 0.13.0 or later) is updated from the Registry; plain `provider` blocks are deprecated since
  Terraform 0.13.0.
- Other updates: `required_version`, `helm_release` chart versions, image references in `docker_*` and
  `kubernetes_*` resources, and `terraform_version` on `tfe_workspace`.
- `depType` values for targeting rules: `module`, `provider`, `required_provider`, `required_version`,
  `helm_release`, `tfe_workspace`, plus Docker and Kubernetes resource types.
- `.terraform.lock.hcl` is the lock file handled by `lockFileMaintenance`; the page says Renovate performs that
  maintenance itself without calling the package manager.

## Ansible Galaxy manager
- Updates dependencies in files used by the `ansible-galaxy` CLI.
- Default file match is the regex `/(^|/)(galaxy|requirements)(\.ansible)?\.ya?ml$/`; extend it with
  `managerFilePatterns`.
- `depType` values: `galaxy-collection` and `role`. Datasources: `galaxy-collection`, `git-tags`, `github-tags`.

## Using them
Create `packageRules` that match on the manager name (`terraform`, `ansible-galaxy`) or on a `depType` above, and read
the Renovate configuration options page for grouping, scheduling, automerge and release-age settings before relying on
any of them. Keep CI (plan, check mode, tests) as a required status check before any automerge.

## Checked
2026-11-01. Confirmed on the Renovate terraform and ansible-galaxy manager pages: file patterns, datasources,
dependency kinds, depTypes, lock file, default requirements match. Removed: the full renovate.json5 example and its
option values (schedule, prConcurrentLimit, minimumReleaseAge, rangeStrategy), execution-environment regex manager,
the separate `ansible` manager description (page text not readable), hostRules advice and terraform-binary claims.
Method: documentation only; no commands were run.
