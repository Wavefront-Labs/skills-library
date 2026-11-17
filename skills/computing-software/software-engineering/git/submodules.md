---
id: computing-software.software-engineering.git.submodules
name: submodules
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, git-submodules, submodule, gitmodules, vendoring, dependencies]
level: practitioner
status: verified
description: "Add, clone, update and remove Git submodules safely, and avoid the detached-HEAD and forgotten-pointer traps that break builds."
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

# Git submodules

**Goal:** pin another repository at an exact commit inside yours, and have every clone and CI run get the same tree.

## 1. Add
```bash
git submodule add -b main https://github.com/org/lib.git vendor/lib
git commit -m "Add lib submodule"
```
This writes `.gitmodules` (url, path, optional branch) and a **gitlink** entry: the parent records a commit SHA, not a branch.

## 2. Clone and update
```bash
git clone --recurse-submodules <url>
git submodule update --init --recursive          # after a plain clone or a pull that moved pointers
git config --global submodule.recurse true       # commands with --recurse-submodules (except clone) recurse by default
```
`update` checks out the recorded SHA in **detached HEAD**. That is correct, not a bug.

## 3. Bump a submodule
```bash
git -C vendor/lib fetch && git -C vendor/lib checkout v1.8.0
git add vendor/lib && git commit -m "Bump lib to v1.8.0"
# or follow the configured branch:
git submodule update --remote vendor/lib
```
Review bumps with `git diff --submodule=log` (or `git config diff.submodule log`).

## 4. Work inside a submodule
`git -C vendor/lib switch -c fix` before committing, push the submodule first, then commit the new pointer in the parent. Guard against pushing a parent pointing at unpushed commits:
```bash
git push --recurse-submodules=check      # or =on-demand; config push.recurseSubmodules
```

## 5. Run across all
```bash
git submodule foreach --recursive 'git status --short'
git submodule status                     # leading '-' = not initialised, '+' = checked out SHA differs from recorded
```

## 6. Remove cleanly
```bash
git submodule deinit -f vendor/lib
git rm -f vendor/lib
```
`deinit` unregisters the submodule and empties its working tree; `git rm` removes the gitlink and its `.gitmodules` section and stages the change. The cloned repository stays under `.git/modules/` in your local clone until you delete it yourself.

## Gotchas
- Changing a URL in `.gitmodules` needs `git submodule sync --recursive` on existing clones.
- A relative URL (`../lib.git`) in `.gitmodules` is resolved against the superproject's default remote, so forks and clones over SSH or HTTPS pick the matching location.
- CI jobs must clone with submodules (`--recurse-submodules` or `git submodule update --init --recursive`) and have credentials that can read private submodules.
- Consider subtree or a package manager if consumers will not tolerate the extra commands.

## Verify
- Fresh `git clone --recurse-submodules` then `git submodule status --recursive` shows no `-` or `+` prefixes and the build passes.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Pro Git submodules chapter. Confirmed: `git submodule add -b`, `update --init --recursive`, `update --remote`, `sync`, `foreach`, `deinit -f`, `status` prefixes (`-` not initialised, `+` commit differs from the index, `U` merge conflicts); update checks out the recorded commit on a detached HEAD; `submodule.recurse` semantics; `git push --recurse-submodules=(check|on-demand|only|no)` and `push.recurseSubmodules`; `diff.submodule` and `--submodule=log`; relative URLs resolve against the superproject's default remote; `git rm` removes the gitlink and `.gitmodules` section and leaves the repository in the superproject's git directory. Removed as unconfirmed: the `actions/checkout` remark and the branch-switch gotcha.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed with a local repository as the submodule: `submodule add -b main` writes `.gitmodules` (path, url, branch) and a mode 160000 gitlink; `clone --recurse-submodules` leaves a detached HEAD; `submodule update --init --recursive`; bump by `-C vendor/lib checkout v1.8.0` then `git add`; `diff --submodule=log`; `submodule update --remote`; `submodule status` shows `+` when the checked-out SHA differs; `push --recurse-submodules=check` aborts when the submodule commit is unpushed; `submodule foreach --recursive`; `submodule sync --recursive` copies a changed `.gitmodules` URL into local config; `deinit -f` then `rm -f` empties the directory, stages the removal of the gitlink and the `.gitmodules` section, and leaves `.git/modules`. Remote HTTPS and SSH URLs were not used.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
