---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-user-access
name: woodpecker-user-access
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [users, open-registration, admin, orgs]
level: practitioner
status: docs-checked
description: "Control who can log in to Woodpecker and who is admin with OPEN, ADMIN, ORGS and REPO_OWNERS."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker user access

Woodpecker has no own registration; users come from the forge through OAuth2. Registration is closed by default (`WOODPECKER_OPEN=false`). If open, any account on the forge can log in.

Restriction patterns:

- Closed registration, with users managed through `woodpecker-cli user`.
- Open registration plus admins:

```ini
WOODPECKER_OPEN=false
WOODPECKER_ADMIN=john.smith,jane_doe
```

- Open registration filtered by organization:

```ini
WOODPECKER_OPEN=true
WOODPECKER_ORGS=dolores,dog-patch
```

For GitLab, group names are the `full_path`, and must match exactly; members of `group` are not permitted if you set `group/subgroup`.

`WOODPECKER_ADMIN` is read at server start and only grants admin, never revokes it. To revoke, remove the user in admin settings (or users API) and also remove them from the list, otherwise they become admin again on the next login after a restart.

`WOODPECKER_REPO_OWNERS` limits which repositories are synchronized and usable, such as your company name on GitHub.

`WOODPECKER_ASYNC_REPOSITORY_UPDATE=true` speeds up login for organisations with many repositories at the cost of possibly outdated lists.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed WOODPECKER_OPEN default false, ADMIN grants but never revokes, ORGS with GitLab full_path, REPO_OWNERS and ASYNC_REPOSITORY_UPDATE. Removed: the GitLab Developer role claim, which the page does not state. 

Method: documentation only; no commands were run.
