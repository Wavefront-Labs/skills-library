---
id: computing-software.software-engineering.git.stashing-and-cleaning
name: stashing-and-cleaning
category: computing-software
field: software-engineering
product: git
tags: [git, git-stash, git-clean, stash-pop, stash-apply, untracked-files, context-switching]
level: practitioner
status: verified
description: "Shelve work in progress with git stash (partial, untracked, named), recover dropped stashes, and remove untracked files safely with git clean."
sources: ["https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning", "https://git-scm.com/docs/git-stash", "https://git-scm.com/docs/git-clean"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stashing and cleaning

**Goal:** park unfinished work to switch context without a junk commit, get it back
intact, and clear untracked clutter without deleting something you needed.

## Stash commands that matter
```bash
git stash push -m "wip: parser refactor"     # name it; "WIP on main" x5 is useless later
git stash push -u                            # include untracked files (default excludes them)
git stash push -p                            # choose hunks interactively
git stash push -- src/a.py src/b.py          # only these paths
git stash push --staged                      # only what is staged (Git 2.35+)
git stash list
git stash show -p stash@{1}                  # inspect before applying
git stash apply stash@{1}                    # apply, keep the entry
git stash pop                                # apply and drop if clean
git stash branch fix-xyz stash@{0}           # new branch at the stash's base, then apply
```

## Gotchas
- `pop` with a conflict applies what it can and does NOT drop the stash. Resolve,
  `git add`, then `git stash drop` yourself.
- Staged vs unstaged state is lost on apply unless you use `git stash apply --index`.
- Stashes are local and do not travel with push. Long-lived stashes rot; if it will
  outlive today, make a WIP commit on a branch instead.
- Ignored files are never stashed unless `-a/--all`.
- `git stash branch` is the fix when a stash no longer applies cleanly because the
  branch moved: it recreates the original base.

## Recovering a dropped or cleared stash
Stashes are commits; a dropped one is a dangling commit until gc:
```bash
git fsck --no-reflog | awk '/dangling commit/ {print $3}' \
  | xargs git log --no-walk --format="%h %s" | grep -i "wip\|on "
git stash apply <sha>
```

## git clean
```bash
git clean -nd        # dry run: what would go (files and dirs)
git clean -fd        # remove untracked files and directories
git clean -fdx       # also ignored files (build output, node_modules, .env!)
git clean -id        # interactive
```
`-x` deletes ignored local config such as `.env`; prefer `-X` (only ignored files) when
you just want a clean build. Nothing removed by clean is recoverable through Git.

## Verify
- [ ] `git stash list` empty (or every entry named and intentional) at end of day.
- [ ] Always ran `git clean -n...` before the `-f` variant.

## Checked
- Git 2.46.2: `push -m` shows in `stash list`; untracked files stay put without `-u` and are stashed with it; `push -- path` stashes only that path; `--staged` stashes only the index (2.35.0 release notes); plain `apply` loses the staged state and `--index` keeps it; a conflicting `pop` keeps the entry; ignored files need `-a`; `stash branch` recreates the stash's base; the fsck pipeline found and re-applied a dropped stash; `clean -nd`, `-fd` (keeps ignored), `-fdX` (only ignored) and `-fdx` behave as listed; `clean -d` without `-f` is refused by `clean.requireForce`.
