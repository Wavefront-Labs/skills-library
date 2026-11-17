---
id: computing-software.software-engineering.git.remote-tracking-branches-and-upstreams
name: remote-tracking-branches-and-upstreams
category: computing-software
field: software-engineering
product: git
tags: [git, remote-tracking-branches, git-upstream, fetch-prune, set-upstream, ahead-behind, git-remote, push-default]
level: practitioner
status: verified
description: "Understand origin/main vs main, set and inspect upstreams, see ahead/behind counts, prune stale branches and configure push defaults."
sources:
  - https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches
  - https://git-scm.com/docs/git-fetch
  - https://git-scm.com/docs/git-branch
  - https://git-scm.com/docs/git-switch
  - https://git-scm.com/docs/git-rev-list
  - https://git-scm.com/docs/gitrevisions
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Remote-tracking branches and upstreams

**Goal:** always know how your local branch relates to the remote one, and keep the
list of branches from filling with ghosts.

## Mental model
- `main` - your local branch.
- `origin/main` - a read-only remote-tracking ref: the remote's main as of your LAST
  fetch. It only moves on `fetch`/`pull`/`push`.
- Upstream - the remote-tracking branch your local branch is linked to; it powers
  `git status` ahead/behind, bare `git pull`/`git push` and `@{u}`.

## Setting and inspecting upstream
```bash
git push -u origin feature             # push and set upstream
git branch -u origin/feature           # set for current branch
git switch feature                      # creates a tracking branch if origin/feature is the only match (--guess is the default)
git branch -vv                          # every branch with its upstream; '[gone]' when the upstream ref no longer exists
git rev-list --left-right --count @{u}...HEAD   # commits only in @{u} (left), then only in HEAD (right)
git log --oneline HEAD..@{u}            # incoming commits
git log --oneline @{u}..HEAD            # outgoing commits
```
`git config --global push.autoSetupRemote true` makes the first plain `git push` assume
`--set-upstream` (with `push.default` of `simple`, `upstream` or `current`).

## Pruning
```bash
git fetch --prune                       # drop origin/* refs deleted on the server
git config --global fetch.prune true    # always
```
Branches whose upstream was deleted show `[gone]` in `git branch -vv`; delete them one by
one with `git branch -d <name>`. Use `-d` not `-D`: it refuses to delete unmerged work. Squash-merged branches show as
unmerged; verify on the server before `-D`.

## Push defaults
`push.default=simple` (the default since Git 2.0) pushes the current branch to the same-named branch on the remote (when that is the remote you pull from, the upstream branch must have the same name). Avoid `matching`, which pushes every branch that has a same-named counterpart on the remote.

## Gotchas
- `git status` says "up to date with origin/main" relative to the last fetch, not reality.
  Run `git fetch` first.
- `git pull origin main` while on `feature` merges main into feature; often not intended.
- Several remotes (`origin`, `upstream` for a fork): name them clearly and check
  `git remote -v`.

## Verify
- [ ] `git branch -vv` shows an upstream for every branch you push.
- [ ] `git branch -r` contains no refs for branches deleted on the server.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: `git branch -u/--set-upstream-to` and `-vv` with the `[gone]` marker; `git switch` guesses a tracking branch from a unique remote branch (`--guess` default); `@{u}` / `@{upstream}` (gitrevisions); `git rev-list --left-right --count`; `push.default=simple` default since Git 2.0 and the `matching` mode; `push.autoSetupRemote` semantics; `git fetch --prune` and `fetch.prune`; `branch -d` versus `-D`. Removed as unconfirmed: the Git version for `push.autoSetupRemote` and the awk/xargs pipeline for deleting gone branches.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `push -u` sets upstream; `branch -u`; `branch -vv` shows `[origin/feature]` and `[origin/feature: gone]` after the remote branch was deleted; `rev-list --left-right --count @{u}...HEAD`; `log HEAD..@{u}` and `@{u}..HEAD`; `fetch --prune`; `remote prune origin --dry-run`; `push.autoSetupRemote` makes a plain `git push` of a new branch create the upstream; `git switch <name>` creates a tracking branch from the only matching remote branch; a missing upstream gives `fatal: no upstream configured`. `push.default` semantics are docs only.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
