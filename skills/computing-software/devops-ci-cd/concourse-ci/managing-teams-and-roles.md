---
id: computing-software.devops-ci-cd.concourse-ci.managing-teams-and-roles
name: managing-teams-and-roles
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [teams, set-team, roles, main-team, active-users, destroy-team, auth]
level: practitioner
status: docs-checked
description: "Create and manage teams with fly set-team, the roles config file, the main team's --main-team flags, and fly teams, get-team, rename-team, destroy-team and active-users."
sources:
  - https://concourse-ci.org/docs/auth-and-teams/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fly set-team` creates or updates a team and is run from a login to the `main` team (users with the owner role can also update their own team). Each run sets the team's authorization config as a whole; it is not a stateful merge.

```shell
fly -t example set-team --team-name my-team --local-user foo
fly -t example login -n my-team
```

Pipelines and one-off builds are owned by the team you are logged into, and list commands are scoped to it. New pipelines are hidden from other teams and unauthorized visitors until exposed.

By default the flags configure the owner role. For other roles pass `-c` with a YAML file that has a single `roles:` list, each entry having a `name` and provider config:

```yaml
roles:
  - name: owner
    github:
      users: [ "admin" ]
  - name: member
    github:
      teams: [ "org:team" ]
  - name: viewer
    github:
      orgs: [ "org" ]
    local:
      users: [ "visitor" ]
```

The `main` team is the only admin team and cannot be promoted to from elsewhere. Its set-team flags are instead given to `concourse web` with a `--main-team-` prefix and apply at every web start, so you cannot lock yourself out.

Other commands: `fly active-users` (default last two months, `--since yyyy-MM-dd`), `fly teams` and `fly teams -d` for auth details and members, `fly get-team -n some-team`, `fly rename-team --old-name my-team --new-name cool-team` (main team only), and `fly destroy-team --team-name my-team`. Destroying a team removes its pipelines and one-off builds but orphans workers assigned to it without cleaning their containers or volumes.

## Checked

2026-11-04. Commands, flags, roles file and main team behaviour confirmed on the Managing Teams and The main team pages.

Method: documentation only; no commands were run.
