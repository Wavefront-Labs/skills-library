---
id: computing-software.devops-ci-cd.gitea.repo-mirror
name: repo-mirror
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-push-mirror, gitea, pull-mirror, mirror-github, mirror-gitlab, mirror-bitbucket, post-receive-ssh-mirror, sync-on-push]
level: practitioner
status: docs-checked
description: "Set up Gitea pull mirrors via migration and push mirrors to GitHub, GitLab or Bitbucket with the right token scopes, plus the SSH post-receive workaround."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/repository/repo-mirror.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea repository mirrors

## Pull mirror (remote into Gitea)
Create menu, **New Migration**, pick the service, enter the URL (and credentials if needed), tick **This repository will be a mirror**, **Migrate repository**. It syncs periodically; **Synchronize Now** in repository settings forces it. **Only repositories that do not exist yet can become pull mirrors**; an existing repo cannot be converted.

## Push mirror (Gitea out to a remote)
Settings, Repository, **Mirror Settings**: enter the URL, expand **Authorization** (the password can be an access token), **Add Push Mirror**. **This force pushes and overwrites the remote.** Errors are shown on the page. Gitea 1.18+ adds `Sync when new commits are pushed` (and the periodic sync can be disabled).

## Provider recipes
- **GitHub**: personal access token with `public_repo` (also `workflow` if the repo has GitHub Actions). Create the empty repo on GitHub first, since GitHub cannot create by push; an existing remote works if the history matches. URL `https://github.com/<group>/<project>.git`, username plus token as password.
- **GitLab**: token with `write_repository`; URL `https://<host>/<group_or_name>/<project>.git`; **Username `oauth2`**, token as password.
- **Bitbucket**: app password with Repository Write; URL `https://bitbucket.org/<group_or_name>/<project>.git`; Bitbucket username plus app password.

## SSH remotes
No SSH push mirrors. Workaround: the Gitea user must be able to reach the remote from the shell, then add a `post-receive` git hook in repository settings:
```
#!/usr/bin/env bash
git push --mirror --quiet git@github.com:username/repository.git &>/dev/null &
echo "GitHub mirror initiated .."
```
Output is discarded (`&>/dev/null`).

## Checked
2026-11-03. Every remaining claim confirmed against the Gitea docs page repo-mirror.md (raw markdown, gitea/docs main branch). Removed the advice that failures are silent and to test the push first (only the discarded output is on the page).
Method: documentation only; no commands were run.
