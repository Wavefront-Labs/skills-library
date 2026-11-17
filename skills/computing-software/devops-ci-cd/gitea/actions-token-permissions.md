---
id: computing-software.devops-ci-cd.gitea.actions-token-permissions
name: actions-token-permissions
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-token-permissions, gitea, gitea-token, permissions-clamping, id-token-write, fork-pr-read-only, cross-repository-access, default-permission-mode]
level: advanced
status: docs-checked
description: "Control the Gitea Actions job token GITEA_TOKEN: permissions keyword, scopes, permissive versus restricted default, maximum clamping, fork PRs and cross-repository access."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/actions/token-permissions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GITEA_TOKEN permissions

Each job gets `GITEA_TOKEN` (also `${{ secrets.GITEA_TOKEN }}`) for Git over HTTP(S) and API calls. These settings and `permissions:` affect only this token, not personal access tokens.

## Resolution order
1. `jobs.<job_id>.permissions`
2. top-level `permissions:`
3. the default from owner or repository settings

The result is then clamped by the maximum: `effective = min(requested, maximum)`. With no maximum configured it is `write` for every scope. A maximum saved before `id-token` existed denies it until set to `write`.

## Syntax
```yaml
permissions: read-all   # or write-all
```
```yaml
permissions:
  contents: read
  issues: write
  pull-requests: none
```
Values: `read`, `write`, `none`. Scopes: `contents` (covers `code` and `releases`), `code`, `releases`, `issues`, `pull-requests`, `actions`, `wiki`, `projects`, `packages`, `id-token`. If both `contents` and a granular scope are given the granular one wins. GitHub-only scopes `statuses`, `checks`, `deployments`, `security-events` and `pages` are not supported; `code`, `releases`, `wiki`, `projects` are Gitea additions. `id-token: write` allows OIDC tokens (see `gitea-actions-oidc`); `read` grants nothing.

## Default mode
- **Permissive** (the backwards-compatible default): read and write on most units of the job's repository.
- **Restricted**: read-only for `code`, `releases`, `packages`; nothing else.
Neither includes `id-token`.

## Where configured
Settings, Actions, General for a user, organization or repository. A repository in an organization follows the owner config unless you tick **Override owner-level configuration**. Repository settings appear only after Repository Actions are enabled.

## Limits
- Pushes still need code write and must pass branch protection, including the **Gitea Actions** allowlist (see `gitea-branch-protection`).
- Fork pull request workflows are always read-only for repository contents and get no OIDC token.
- Cross-repository: only the job's repository plus public repositories (read-only). Allow selected private repositories under Settings, Actions, General, **Cross-Repository Access**, or allow selected collaborative owners; fork PR runs never gain it.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page token-permissions.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
