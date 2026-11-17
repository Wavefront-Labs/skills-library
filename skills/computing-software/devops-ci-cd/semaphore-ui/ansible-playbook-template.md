---
id: computing-software.devops-ci-cd.semaphore-ui.ansible-playbook-template
name: ansible-playbook-template
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [ansible, playbook, galaxy, requirements-yml, working-directory, semaphore-ui]
level: practitioner
status: docs-checked
description: "Configure an Ansible Playbook template including working directory, galaxy requirements behaviour and common options."
sources:
  - https://semaphoreui.com/docs/user-guide/apps/ansible
  - https://semaphoreui.com/docs/user-guide/host-config
  - https://semaphoreui.com/docs/faq/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ansible playbook templates

Goal: run `ansible-playbook` from a repository.

Create: Task Templates, New Template, Ansible Playbook. Parameters: repository, playbook path, optional working directory, inventory, variable groups, vaults (Ansible Vault passwords from the Key Store), extra CLI arguments (tags, skip-tags, limit, verbosity) and environment variables.

Working directory: a path relative to the repository root from which Ansible runs, useful for a subdirectory `ansible.cfg`. It affects configuration lookup but does not add that directory's `roles/` or `collections/` to Ansible's search paths by itself.

Galaxy requirements: before a run Semaphore installs roles and collections from `requirements.yml` files found in the playbook directory, repository root and their `roles/` and `collections/` subdirectories. It stores a checksum per file and reinstalls only when the file changes. Two options:
- Skip Galaxy install: never run `ansible-galaxy` (use when requirements are preinstalled in the runner image).
- Force Galaxy install: always `ansible-galaxy install --force`, for moving targets.

Types: Task, Build, Deploy. A Cron schedule can be set on the template; a cron job that polls the repository can trigger a Build task for new commits.

Private role or collection sources need a Host config mapping.

Gotcha: implicit localhost in a container or snap may fail at Gathering Facts. Set `gather_facts: False` or use `ansible_connection=ssh` for localhost.

Verify: the task log shows `ansible-playbook` with the chosen inventory and a green recap.

## Checked

2026-11-04: checked against the Ansible app, host config and troubleshooting pages. Every remaining claim is stated on those pages.

Method: documentation only; no commands were run.
