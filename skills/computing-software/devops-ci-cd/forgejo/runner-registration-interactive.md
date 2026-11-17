---
id: computing-software.devops-ci-cd.forgejo.runner-registration-interactive
name: runner-registration-interactive
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [runner-registration, runner-uuid-token, runner-scope, server-connections]
level: practitioner
status: docs-checked
description: "Register a runner at admin, organization, user or repository level and place the UUID and token in the config."
sources:
  - https://forgejo.org/docs/latest/admin/actions/registration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A runner needs a UUID and a token to connect, which act as username and password. Three methods exist: interactive (recommended), the HTTP API, and offline registration with the CLI.

Interactive registration offers four places, which decide which workflows the runner executes:

- `/admin/actions/runners` (system administrator): all repositories on the instance.
- `/org/{org}/settings/actions/runners`: all repositories of the organization.
- `/user/settings/actions/runners`: all repositories owned by the user.
- `/{owner}/{repository}/settings/actions/runners`: the one repository.

Each list also shows runners inherited from higher levels. Click Create new runner, enter a name and description, and the UUID and token are displayed. Copy them into the runner config's `server` section:

```
server:
  connections:
    forgejo:
      url: https://example.com/
      uuid: <uuid>
      token: <token>
```

Repeat for more connections; keys must be unique but have no meaning, so one runner can serve several instances, organizations, users or repositories.

Each runners page also lists runners from higher-level registrations, so a repository's list includes organization-level and system administrator-level runners. Copy the displayed UUID and token into the connections entry of the server section of the runner configuration, together with the Forgejo URL.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Runner Registration" page, read in full including its code blocks: the three registration methods, the four registration URLs and their scopes, the inherited runner lists, the Create new runner dialog, the `server.connections` example and the note that keys must be unique but have no meaning.
Corrected: nothing needed; every claim matched the page text. The skill repeats the inherited-runners point in its last paragraph (thin, redundant).
Method: documentation only; no commands were run.
