---
id: computing-software.devops-ci-cd.semaphore-ui.host-config-credential-mapping
name: host-config-credential-mapping
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [host-config, submodules, requirements-yml, private-modules, credentials, semaphore-ui]
level: advanced
status: docs-checked
description: "Map hosts and URL prefixes to Key Store credentials so submodules, private roles and Terraform modules authenticate."
sources:
  - https://semaphoreui.com/docs/user-guide/host-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host config

Goal: give tasks the right credential for servers other than the main repository.

A repository has exactly one key. Anything else a task touches (private submodules on another Git server, roles in `requirements.yml`, private Terraform or OpenTofu modules, an inventory repository, inventory hosts needing a different SSH key) fails with Permission denied or Authentication failed unless mapped.

A mapping has a match (host name or URL prefix) and a Key Store credential. Examples from the docs:

| Case | Mapping |
|---|---|
| Submodule `git@gitlab.example.com:infra/common.git` | Host `gitlab.example.com` to an SSH key |
| Role `https://gitlab.example.com/ansible/role-nginx.git` | URL prefix to a login/token credential |
| Terraform module `git::https://github.com/acme/tf-modules.git` | URL prefix `https://github.com/acme/` to an SSH key or a token |
| Inventory hosts `db-01.internal` | Host to an SSH key |

Semaphore installs the project's mappings before the task starts. One mapping serves all templates, and if a project has no mappings behaviour is unchanged.

Steps: open the project's Host config page (project menu, below Repositories), press Add mapping, choose the Key Store credential, save, and re-run.

Gotchas:
- When several URL mappings match, the most specific URL wins, so a one-repository mapping overrides its group mapping.
- A Host mapping needs an SSH key. A URL mapping takes an SSH key (the URL is rewritten to SSH form) or a Login with password (https URLs only; leave the login empty to use a personal access token).
- Mappings need the default `git_client: cmd_git`; with `go_git` a task of a project with mappings fails.
- A Key Store key referenced by a mapping cannot be deleted.

Verify: the previously failing `git submodule update`, `ansible-galaxy install` or `terraform init` succeeds.

## Checked

2026-11-04: checked against the host config page. Added the trailing-slash URL form, most-specific-URL rule, key and login types, git_client requirement and delete restriction; corrected the menu location.

Method: documentation only; no commands were run.
