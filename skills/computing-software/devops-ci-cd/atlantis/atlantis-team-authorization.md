---
id: computing-software.devops-ci-cd.atlantis.atlantis-team-authorization
name: atlantis-team-authorization
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [team-authz, gh-team-allowlist, permissions, external-command, production-gating]
level: advanced
status: docs-checked
description: "Restrict who can run Atlantis commands per repo and project with gh-team-allowlist or an external team_authz command."
sources: ["https://www.runatlantis.io/docs/repo-and-project-permissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis team authorization

Atlantis runs two checks. The repository-level check runs after a command is validated and before var files, repo metadata or PR statuses are checked. The project-level check runs after pre-workflow hooks, repo config processing and affected-project detection. Two checks exist because hooks may generate the config, so affected projects are unknown at the first check.

Option 1: `--gh-team-allowlist`, a global setting for all repos, for example `--gh-team-allowlist="*:plan,*:policy_check,myteam:apply"`. If policy checking is on, allowlist `policy_check` as well.

Option 2: an external command under `team_authz` in server-side repo config (`command`, optional `args`). If it is defined, `--gh-team-allowlist` is ignored. Atlantis runs it on every check as:

```text
external_command [external_args...] atlantis_command repo [teams...]
```

Environment includes `BASE_REPO_NAME`, `BASE_REPO_OWNER`, `COMMAND_NAME`, `USER_NAME`; project checks add `PROJECT_NAME`, `PULL_NUM`, `HEAD_BRANCH_NAME`, `REPO_ROOT`, `REPO_REL_PATH`, `COMMENT_ARGS` and more.

The user is authorized only if the command exits 0 and the last output line is `pass`. A non-zero exit means the command could not evaluate (bad config, missing dependency). If it ran fine but the user is not allowed, still exit 0 and print a reason. A typical script passes everything except `apply` on the `prod` project, which requires membership in a prod deployers team.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Repo and Project Permissions. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
