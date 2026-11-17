---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.infrastructure-repo-layout-and-branching-strategy
name: infrastructure-repo-layout-and-branching-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, infra-repo-layout, environment-directories, blast-radius, ansible-layout]
level: advanced
status: docs-checked
description: "Lay out infrastructure repositories: separate state per environment (directories or workspaces) for Terraform, and the documented Ansible inventory and role layouts."
sources: ["https://developer.hashicorp.com/terraform/tutorials/modules/organize-configuration", "https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infrastructure repo layout

Goal: anyone can answer "what is deployed in prod and where is its code" from the repo alone, changes have a small blast radius, and promotion between environments is explicit.

## Terraform: split state as the project grows
HashiCorp's organize-configuration tutorial walks a project from a monolith (one main configuration, one state file) to independent configuration and state per environment.
- Several environments defined in one configuration is hard to manage as it grows, and can hide cross-environment dependencies. In the tutorial a shared `random_pet` resource referenced by both dev and prod meant changing it in the dev file destroyed and recreated both environments' resources.
- Using `-target` to scope operations in a monolith is described as risky and not a sustainable way to manage distinct environments.
- Two primary ways to separate state between environments: directories and workspaces. Use directories for environments that may differ in configuration; use workspaces for environments that do not deviate much, to avoid duplicating configuration.
- Directories shrink the blast radius, because Terraform operates only on the state and configuration in the working directory by default. The trade-off: duplicated code can drift between environments over time. Moving an existing single-state project into directory-separated states needs advanced state operations to move the resources.
- State separation signals more mature usage but adds complexity.

## Ansible: documented sample layouts
The Ansible sample setup is explicitly one approach to adapt, not a rule.
- Single-inventory-per-environment layout: one inventory file per environment (`production`, `staging`) at the top level with `group_vars/` and `host_vars/` beside them, top-level playbooks (`site.yml` plus per-tier playbooks such as `webservers.yml`), and most tasks in `roles/`.
- Alternative layout: an `inventories/` directory with a subdirectory per environment, each holding its own `hosts`, `group_vars/` and `host_vars/`. This gives total separation of inventory variables between environments and more flexibility for large environments, but is harder to maintain because there are more files.
- `site.yml` can import per-tier playbooks with `import_playbook`; run `site.yml` for everything or a tier playbook for part (similar to `--limit`).
- By default playbooks sit in one directory with `roles/` beneath it. If you move playbooks into a `playbooks/` subdirectory, set `roles_path` in `ansible.cfg`.
- Defaults that are universally true go in `group_vars/all`; per-system hardware variance goes in `host_vars`.
- The `hostvars` variable reads host-specific variables only, not group variables.

## Gotchas
- Keep environment directories thin (module calls plus values) so that copies do not drift; logic belongs in modules or roles.
- Moving or renaming a state directory is a state migration; plan it as a change, not a refactor.

## Verify
- [ ] For any prod resource, you can find the directory and module version that manages it.

## Checked
Method: docs-checked 2026-11-09 against the HashiCorp "organize configuration" tutorial (read the intro and state-separation sections) and the Ansible "Sample Ansible setup" page.
Removed as unconfirmed (Gruntwork source not read): the trunk-based versus branch-per-environment recommendation, CODEOWNERS and branch protection advice, the monorepo versus polyrepo table, and the `live/` region directory tree. The description and tags were adjusted to match.
