---
id: computing-software.software-engineering.git.forking-workflow-and-syncing-forks
name: forking-workflow-and-syncing-forks
category: computing-software
field: software-engineering
product: git
tags: [git, distributed-workflows, forking-workflow, sync-fork, integration-manager, pull-requests, upstream-remote, open-source]
level: practitioner
status: verified
description: "Contribute through a fork: upstream/origin remotes, topic branches, keeping the fork in sync, and updating a PR without wrecking reviewers' history."
sources:
  - https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows
  - https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
  - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forking workflow and syncing a fork

**Goal:** contribute to a repository you cannot push to (integration-manager workflow) while keeping your fork current and your pull requests reviewable.

## 1. Remotes
```bash
git clone git@github.com:me/project.git && cd project
git remote add upstream https://github.com/org/project.git
git remote set-url --push upstream DISABLED      # guard against pushing to upstream by accident
git remote -v
```
Convention: `origin` = your fork (read/write), `upstream` = canonical repo (read-only).

## 2. One topic branch per change, cut from upstream
```bash
git fetch upstream
git switch -c fix-timeout upstream/main
# ...commit...
git push -u origin fix-timeout          # then open the PR from me:fix-timeout -> org:main
```
Never commit on your fork's `main`. Keep it a pure mirror so syncing is always a fast-forward.

## 3. Sync the fork
```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main       # fails loudly if you committed on main by mistake
git push origin main
```
GitHub alternative: `gh repo sync me/project` or the "Sync fork" button (also ff-only unless you discard commits).

## 4. Update an open PR when upstream moves
- Project prefers linear history: `git rebase upstream/main` then `git push --force-with-lease`.
- Project says "don't force-push during review": `git merge upstream/main` and push normally.
- Address review comments as new commits (`fixup!` via `git commit --fixup=<sha>`), squash with `git rebase -i --autosquash` only when the reviewer is done.

## Integration-manager side
Maintainer fetches the contributor's branch without adding a remote:
```bash
git fetch https://github.com/contrib/project.git fix-timeout
git log --oneline main..FETCH_HEAD
git merge --no-ff FETCH_HEAD
```
Or check out PRs directly: `gh pr checkout 123`, or `git fetch upstream pull/123/head:pr-123`.

Checked in a scratch bare-remote setup: the `DISABLED` push URL makes `git push upstream` fail, `merge --ff-only` and `rev-list --left-right --count` behave as described, and `gh repo sync` is a fast-forward unless `--force` (hard reset) per `gh repo sync --help`.
## Gotchas
- `--force` instead of `--force-with-lease` can erase a co-maintainer's "allow edits from maintainers" commit.
- Forks of private repos inherit visibility and are deleted when access is removed.
- Long-lived fork drift: if you carry patches, rebase them onto upstream on a schedule, not once a year.
- GitHub Actions in forks do not get the base repo's secrets on `pull_request`; don't "fix" this with `pull_request_target` plus checkout of PR code.

## Verify
- `git log --oneline upstream/main..main` is empty (fork main has nothing extra).
- `git rev-list --left-right --count upstream/main...fix-timeout` shows 0 behind before requesting review.
