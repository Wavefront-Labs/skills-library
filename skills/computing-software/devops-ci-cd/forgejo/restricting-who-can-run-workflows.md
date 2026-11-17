---
id: computing-software.devops-ci-cd.forgejo.restricting-who-can-run-workflows
name: restricting-who-can-run-workflows
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [disable-registration, max-creation-limit, runner-scope, branch-protection-bypass]
level: advanced
status: docs-checked
description: "Reduce Actions attack surface with app.ini access limits, narrow runner registration scope and 2FA."
sources:
  - https://forgejo.org/docs/latest/admin/actions/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The security guide models an attacker who wants to run custom workflows and works through layers of defence.

Access settings in app.ini:

- `service.DISABLE_REGISTRATION = true` stops unexpected registrations; admins create accounts.
- `repository.MAX_CREATION_LIMIT = 0` stops users creating repositories to run workflows in; admins can override temporarily. For other values except -1 and 0, also set `admin.DISABLE_REGULAR_ORG_CREATION = true`, since organizations bypass the limit.
- `repository.ALLOW_FORK_WITHOUT_MAXIMUM_LIMIT = false` prevents forking, which blocks pull requests that trigger workflows.

On small instances review Admin settings > Identity & access > User accounts and ensure 2FA is on. Keeping the instance on a local network or VPN is another layer.

Register runners at the tightest level: repository runners only run that repository's workflows, organization or user runners only their repositories, global runners any repository.

Anyone who can push to any new branch can run workflows even with branch protection, since a new branch can carry its own workflow. Ephemeral runners are advised where runners are created on demand, particularly in host mode, because the runner token is then visible to the job.

## Checked

2026-11-04. Confirmed against the Forgejo Securing Forgejo Actions Deployments page (Forgejo Access, Runner Registration, Ephemeral Runners, Preventing Arbitrary Workflow Execution): all four app.ini settings, the 2FA review path, the VPN layer, the runner scopes, the new-branch workaround and ephemeral runners. Nothing removed.

Method: documentation only; no commands were run.
