---
id: computing-software.devops-ci-cd.semaphore-ui.terraform-workspaces-and-http-backend
name: terraform-workspaces-and-http-backend
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [terraform-workspaces, http-backend, state-locking, tfstate, pro, semaphore-ui]
level: advanced
status: docs-checked
description: "Create Terraform workspaces and use the built-in Pro HTTP backend for state storage, locking and versions."
sources:
  - https://semaphoreui.com/docs/user-guide/apps/terraform/workspaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Terraform workspaces and HTTP backend

Goal: separate environments and let Semaphore store state.

Workspaces: open the template's Workspaces tab, click the plus button, New Workspace, enter a name and select an SSH key (or None). Each workspace has isolated state; MAKE DEFAULT sets the default one. Semaphore does not currently support workspace-specific variables.

HTTP backend (Pro): stores state inside Semaphore with state locking, version history and UI management. Template option Override backend settings avoids editing code, and an optional configuration file name can be set for the generated backend file.

Use outside Semaphore: set an alias (a unique HTTP endpoint) on the Workspaces tab, with a key holding a username and password, then point a Terraform `backend "http"` block at that URL.

Gotchas:
- The HTTP backend and its aliases need the Pro edition.

## Checked

2026-11-07. Read in full: user-guide/apps/terraform/workspaces.md and states.md. Confirmed: the create flow, state isolation, MAKE DEFAULT, Pro HTTP backend with locking, versions and UI, backend override, optional config file name, aliases with a key, the backend "http" block. Corrected: the draft claimed workspace-specific environment variables; workspaces.md says they are not supported. Removed: the invented Verify step.
Method: documentation only; no commands were run.
