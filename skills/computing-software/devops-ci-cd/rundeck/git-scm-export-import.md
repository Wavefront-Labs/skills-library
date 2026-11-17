---
id: computing-software.devops-ci-cd.rundeck.git-scm-export-import
name: git-scm-export-import
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, scm-git, git-export, git-import, uuid-behavior]
level: practitioner
status: docs-checked
description: "Configure Rundeck's Git SCM export and import plugins: repository URL forms, committer, UUID behavior, file path template and authentication from Key Storage."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/scm/git.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open Project Settings, Setup SCM, then choose Export or Import.

Repository: **Base Directory** is a local clone folder on the server. URL forms the plugin needs:
- HTTP(S): `https://scm-user@host.xz/path/to/repo.git`
- SSH: `ssh://git@host.xz/path/to/repo.git`. A clone URL like `git@host.xz:path/to/repo.git` must be rewritten: prepend `ssh://` and replace the `:` with `/`.

Gotcha: an invalid URL can make Rundeck behave erratically.

Export: Committer Name and Email are mandatory (default `${user.fullName}` and `${user.email}`). **Export UUID Behavior**: `preserve`, `original` or `remove`; changing it means re-pushing files. **Import UUID Behavior**: `preserve`, `archive` or `remove`. **File Path Template** tokens: `${job.name}`, `${job.group}`, `${job.project}`, `${job.id}`, `${job.sourceId}`, `${config.format}` (xml, yaml or json).

Authentication: SSH Key Storage Path or Password Storage Path (both from Key Storage), optional strict host key checking. If the user lacks permission to that key, the plugin is disabled for the project with an "SCM disabled" error in GUI and logs.

Versions before 4.5 cannot use private-key auth to GitHub; use Password with a personal access token. Fetch automatically should be true; "Synchronize/Pull automatically" never imports jobs; do imports manually.

Import adds Match a Regular Expression to pick files.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Git Plugin: Setup SCM location, Base Directory, HTTP(S) and SSH URL forms and the ssh:// rewrite tip, invalid URL warning, mandatory committer fields and defaults, Export UUID Behavior and Import UUID Behavior values, File Path Template tokens, Key Storage authentication, the SCM disabled message, the pre-4.5 GitHub private key limitation, fetch and manual import advice, and Match a Regular Expression. Nothing removed.

Method: documentation only; no commands were run.
