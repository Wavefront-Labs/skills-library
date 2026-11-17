---
id: computing-software.devops-ci-cd.semaphore-ui.task-template-form
name: task-template-form
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [task-templates, templates, repository, inventory, task-runner, semaphore-ui]
level: practitioner
status: docs-checked
description: "Understand task template types (Task, Build, Deploy), the template list, tabs and the common form fields."
sources:
  - https://semaphoreui.com/docs/user-guide/task-templates
  - https://semaphoreui.com/docs/user-guide/projects/history
  - https://semaphoreui.com/docs/reference/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Task templates

Goal: define what runs and how.

A template names the application, repository and file, inventory, variable groups, credentials and the options users may change at launch. Supported apps: Ansible, Terraform/OpenTofu, Terragrunt, Bash, PowerShell, Python.

Create and edit needs the Manager role or higher (New Template, pencil icon).

Types:

| Type | Purpose |
|---|---|
| Task | A plain run (default). |
| Build | Produces an artifact with an auto-incremented version. |
| Deploy | Deploys a build version. |

Common fields: Name (required), Description, App, Repository, Branch (empty uses the repository's branch), and Playbook or Script filename relative to the repository root (for Terraform apps, the subdirectory with the code). Further groups hold inventory, variable groups, schedules, alerts, prompts and survey variables.

The list shows name (play button starts a task), version or last result, status, last task, playbook, inventory, variable groups and repository. Gear icon chooses columns; tabs above the list are views (named groups of templates).

On a template page: Run/Build/Deploy button, Stop all, and tabs Tasks (with rerun), Details (with the status chart) and Workspaces (Terraform family only).

Gotchas:
- Disable or enable apps in the Applications page; a disabled app is hidden from the form but existing templates keep working.
- `max_tasks_per_template` (config or `SEMAPHORE_MAX_TASKS_PER_TEMPLATE`) is history retention: the maximum number of recent tasks stored per template, not a concurrency limit.
- Tasks of one template run sequentially by default; the "Allow parallel tasks" template option lets them run at the same time.

## Checked

2026-11-07. Read in full: user-guide/task-templates/README.md and user-guide/apps/README.md; the max_tasks_per_template meaning from reference/configuration.md (the matching table row only) and user-guide/projects/history.md. Confirmed: roles, types, common fields, list columns, template page tabs, Applications behaviour, parallel-tasks default. Corrected: the draft said max_tasks_per_template limits concurrency; it is history retention. Removed: the invented Verify step.
Method: documentation only; no commands were run.
