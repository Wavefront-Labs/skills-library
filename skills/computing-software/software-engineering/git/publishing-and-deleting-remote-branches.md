---
id: computing-software.software-engineering.git.publishing-and-deleting-remote-branches
name: publishing-and-deleting-remote-branches
category: computing-software
field: software-engineering
product: git
tags: [git, push-upstream, delete-remote-branch, git-push, push-default, autosetupremote, remote-branches]
level: practitioner
status: verified
description: "Publish a local branch with push -u, set push.default/autoSetupRemote, push to a different remote name, delete remote branches and tags, and clean up stale remote-tracking refs."
sources:
  - https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/git-fetch
  - https://git-scm.com/docs/git-remote
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Publishing and deleting remote branches

**Goal:** get branches onto (and off) the shared remote predictably, with upstream
tracking set so plain `git push` / `git pull` do the right thing.

## Publishing
```bash
git push -u origin feature/login          # push and set upstream (branch.<name>.merge)
git push origin feature/login:review/login  # push under a different remote name
git push origin HEAD                      # current branch, same name
```
Make first push effortless:
```bash
git config --global push.default simple        # default since 2.0: push current to same-named upstream
git config --global push.autoSetupRemote true  # plain `git push` assumes --set-upstream when none exists
```
`push.autoSetupRemote` takes effect with `push.default` set to `simple`, `upstream` or `current`. A plain `git push` from a branch with no upstream fails with a "no upstream branch" error unless one of the above was done.

## Deleting on the remote
```bash
git push origin --delete feature/login    # modern
git push origin :feature/login            # refspec form: push "nothing" to it
git push origin --delete v1.2.0-rc1       # same for tags (or :refs/tags/v1.2.0-rc1)
```
A server can refuse deletion (for example `receive.denyDeletes`, or a hosting service's branch protection); change the protection rules first.

## Cleaning up everyone's view
Other clones keep `origin/feature/login` until they prune:
```bash
git fetch --prune                     # or once: git config --global fetch.prune true
git remote prune origin --dry-run
```
Pruned tags need `fetch.pruneTags true` (be careful: deletes local tags missing remotely).

## Gotchas
- `git push --all` pushes every local branch, including experiments. Prefer explicit names.
- `git push --mirror` makes the remote match local refs exactly: refs deleted locally are
  deleted on the remote. Only for repository mirroring or migration.
- If a short destination name could be either a branch or a tag, push errors out as
  ambiguous; spell out `refs/heads/<name>` or `refs/tags/<name>`.

## Verify
- [ ] `git branch -vv` shows `[origin/<branch>]` after first push.
- [ ] `git ls-remote --heads origin <branch>` empty after deletion.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: `push.default=simple` default since Git 2.0 (config/push); `push.autoSetupRemote` semantics and the `simple`/`upstream`/`current` condition; `git push --delete`, the empty-source `:<dst>` deletion refspec, `--mirror` deleting remote refs, `-u/--set-upstream`; `git remote prune [-n]` and `fetch.prune` / `fetch.pruneTags` (config/fetch; pruneTags behaves as the `refs/tags/*:refs/tags/*` refspec). Removed as unconfirmed: the Git version for `push.autoSetupRemote`, the exact fatal message text and the note about hosts auto-deleting merged branches.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `push -u origin <branch>`; `push origin local:remote`; `push origin HEAD`; `push origin --delete <branch>` and `push origin :<branch>`; `push origin --delete <tag>`; `ls-remote --heads origin <branch>` empty after deletion; `fetch --prune` and `remote prune --dry-run`; `branch -vv` shows `[origin/<branch>]`; `push --mirror`; deleting the current branch of a remote is refused by the server. `receive.denyDeletes` and hosting-service protection are docs only.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
