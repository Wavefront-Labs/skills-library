---
id: computing-software.software-engineering.git.updating-and-removing-submodules
name: updating-and-removing-submodules
category: computing-software
field: software-engineering
product: git
tags: [git, submodule-update-remote, submodule-deinit, git-submodules, absorbgitdirs, submodule-url-change, submodule-maintenance]
level: advanced
status: verified
description: "Maintain submodules over time: bump to upstream with update --remote, track a branch, change URLs with sync, remove cleanly with deinit and rm, and absorb nested .git dirs."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Submodules
  - https://git-scm.com/docs/git-submodule
  - https://git-scm.com/docs/gitmodules
  - https://git-scm.com/docs/git-rm
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Updating and removing submodules

**Goal:** the maintenance side of submodules: moving pins forward, renaming URLs and
deleting a submodule without leftovers that break future clones.

## Bumping to upstream
```bash
git submodule update --remote libs/parser          # fetch and check out tracked branch tip
git -C libs/parser log --oneline -3                # what you are pinning
git add libs/parser && git commit -m "Bump parser to 1a2b3c4 (fixes #88)"
```
Track a branch other than the remote HEAD:
```bash
git config -f .gitmodules submodule.libs/parser.branch release-2.x
```
Or manually: `cd libs/parser && git fetch && git checkout v2.4.1 && cd - && git add libs/parser`.
The superproject stores only the commit (gitlink); the commit you pin must be pushed to the
submodule's remote or others cannot fetch it. Guard it:
`git push --recurse-submodules=check` (or `on-demand`).

## Pulling others' bumps
```bash
git pull && git submodule update --init --recursive
git config --global submodule.recurse true     # commands with --recurse-submodules (except clone) recurse by default
```

## Changing a submodule URL
```bash
git config -f .gitmodules submodule.libs/parser.url https://git.example.org/parser.git
git submodule sync --recursive      # copy the .gitmodules URL into local config of already-initialised submodules
git submodule update --init --recursive
git commit -am "Move parser submodule to new host"
```

## Removing a submodule completely
```bash
git submodule deinit -f libs/parser        # unregister, empty the working dir
git rm -f libs/parser                      # remove gitlink + .gitmodules section, staged
git commit -m "Remove parser submodule"
```
`git rm` leaves the submodule's cloned repository under `.git/modules/` in your local clone;
delete that directory yourself if you want it gone.

## absorbgitdirs
A submodule whose git directory is inside its own working tree (an independently cloned
repository added later, or an old clone) can have it moved into the superproject's
`$GIT_DIR/modules` so the submodule can be removed or moved safely:
```bash
git submodule absorbgitdirs
```

## Verify
- [ ] `git submodule status --recursive` shows no `-` (uninitialised) or `+` (checked out commit differs) markers.
- [ ] CI clones with `--recurse-submodules` and the pinned commits resolve.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: `git submodule update --remote`, `submodule.<name>.branch` in `.gitmodules` (defaults to the remote HEAD), `sync [--recursive]` semantics, `deinit -f`, `git rm` on a submodule (removes the work tree and the `.gitmodules` section, stages it), `absorbgitdirs`, `push --recurse-submodules=(check|on-demand)` and `submodule.recurse`. Removed as unconfirmed: the exact `reference is not a tree` and `A git directory ... is found locally` messages, the claim that `rm -rf .git/modules/<path>` is required, and the statement that sync also rewrites the submodule's own config.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed with a local repository as the submodule: `submodule update --remote`; `git -C <path> log`; `config -f .gitmodules submodule.<path>.branch`; `submodule sync --recursive` after changing `.gitmodules` url; `git submodule absorbgitdirs` succeeds; `deinit -f` plus `rm -f` leaves `.git/modules` in place; `submodule.recurse` and `push --recurse-submodules=check` as in the submodules skill.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
