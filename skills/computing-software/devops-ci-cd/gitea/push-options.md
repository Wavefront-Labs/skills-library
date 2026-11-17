---
id: computing-software.devops-ci-cd.gitea.push-options
name: push-options
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-push-options, gitea, push-to-create, repo-private-option, default-push-create-private, enable-push-create-user]
level: practitioner
status: docs-checked
description: "Gitea push features: the compare-link hint, repo.private and repo.template push options, and push-to-create with ENABLE_PUSH_CREATE_USER and ORG settings."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/repository/push.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea push features

## Compare hint
Pushing a non-default branch for the first time prints a link to the compare page against your main branch, from which you can open a PR targeting any branch.

## Push options (Gitea 1.13+)
- `repo.private` (true|false): change visibility.
- `repo.template` (true|false): change whether the repository is a template.
```shell
git push -o repo.private=false -u origin main
```
Especially useful with push-to-create, where new repositories otherwise get the default visibility. (AGit pull requests use other `-o` options; see `gitea-agit-flow`.)

## Push to create
Push to a repository that does not exist yet. **Disabled by default.** In `app.ini` set `ENABLE_PUSH_CREATE_USER = true` (own account) and/or `ENABLE_PUSH_CREATE_ORG = true` (organizations the user belongs to), then restart Gitea. Both are in the `[repository]` config section.
```shell
git remote add origin git@{domain}:{username}/{repo name that does not exist yet}.git
git push -u origin main
```
SSH and HTTPS remotes both work. Visibility of the created repo follows `DEFAULT_PUSH_CREATE_PRIVATE` in `app.ini`; override it in the same push with `-o repo.private=true|false`.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
