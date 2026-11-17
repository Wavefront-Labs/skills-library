---
id: computing-software.software-engineering.git.multiple-working-trees-with-worktree
name: multiple-working-trees-with-worktree
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, git-worktree, parallel-branches, worktrees, code-review]
level: practitioner
status: verified
description: "Check out several branches at once with git worktree for reviews, hotfixes and parallel agents, and clean up stale or locked worktrees."
sources:
  - https://git-scm.com/docs/git-worktree
  - https://git-scm.com/docs/git-config#Documentation/git-config.txt-worktreeguessRemote
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple working trees with git worktree

**Goal:** work on a hotfix, review a PR, or run a long build on another branch without stashing or re-cloning.

## 1. Create
```bash
git worktree add ../proj-hotfix -b hotfix/1.4.1 origin/release-1.4   # new branch from a start point
git worktree add ../proj-review pr-123                                 # existing branch
git worktree add --detach ../proj-bisect v1.3.0                        # no branch, for experiments
```
All worktrees share one object store and refs; only `HEAD`, the index and working files are per-worktree. Creation is cheap and fetches are shared.

## 2. List, move, remove
```bash
git worktree list --porcelain
git worktree move ../proj-review ../proj-pr-123
git worktree remove ../proj-hotfix          # refuses if dirty; --force to discard
git worktree prune                          # forget worktrees whose directories were deleted by hand
git worktree lock --reason "on USB disk" ../proj-usb
```

## 3. Rules Git enforces
- A branch can be checked out in only one worktree at a time ("fatal: 'main' is already used by worktree at ..."). Use `--detach` or a new branch.
- `git branch -d` refuses to delete a branch checked out in another worktree.
- Rebasing a branch that another worktree has checked out is blocked for the same reason.

## 4. Per-worktree config
```bash
git config extensions.worktreeConfig true
git config --worktree core.sparseCheckout true      # stored in .git/worktrees/<name>/config.worktree
```
Useful for sparse checkouts or different hooks per worktree.

## Practical patterns
- Keep worktrees as siblings (`../proj-<task>`), never inside the main checkout, so tools and globs do not recurse into them.
- One worktree per concurrent agent or CI job on a shared machine; each gets its own index, avoiding `index.lock` contention.
- Dependencies (`node_modules`, `target/`, `.venv`) are per-worktree; budget disk accordingly.

## Gotchas
- Deleting the directory with `rm -rf` leaves metadata; run `git worktree prune`.
- Submodules in linked worktrees need their own `git submodule update --init`.
- Hooks are shared (they live in the common dir) unless `core.hooksPath` differs per worktree config.

## Verify
- `git worktree list` shows each path with the expected branch; `git -C ../proj-hotfix status` is clean after removal of temporary work.

## Checked
- Git 2.46.2 with a bare origin: `add -b`, `add <branch>`, `add --detach <tag>` all create worktrees and `list`/`--porcelain` show them; `fatal: 'main' is already used by worktree at ...`; `branch -d` and `rebase` refuse a branch used elsewhere; `move` works, `remove` refuses a dirty tree until `--force`; deleting a directory leaves an entry until `prune`; `lock --reason` makes `remove` fail with the reason; `extensions.worktreeConfig` plus `config --worktree` writes `.git/worktrees/<name>/config.worktree` and leaves the main worktree unset; a hook in the common `.git/hooks` ran from a linked worktree. Disk budgeting and submodule notes are not tested.
