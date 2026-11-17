---
id: computing-software.software-engineering.git.undoing-changes-restore-reset-revert
name: undoing-changes-restore-reset-revert
category: computing-software
field: software-engineering
product: git
tags: [git, undoing-changes, git-restore, git-revert, undo-commit, git-reset, git-switch, discard-changes, unstage]
level: practitioner
status: verified
description: "Pick the right Git undo: restore for working-tree/index, reset for local commits, revert for shared history, and how to undo each undo."
sources: ["https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things", "https://git-scm.com/docs/git-restore", "https://git-scm.com/docs/git-revert", "https://git-scm.com/docs/git-reset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undoing changes: restore, reset or revert

**Goal:** undo exactly the layer you meant (working tree, index, or commits) without
destroying work, and never rewrite history other people already pulled.

## Decision table
| You want to... | Command | Safe on pushed history? |
|---|---|---|
| Discard unstaged edits to a file | `git restore <path>` | yes (local only) |
| Unstage a file, keep the edits | `git restore --staged <path>` | yes |
| Get a file back as it was N commits ago | `git restore --source=HEAD~3 <path>` | yes |
| Drop the last local commit, keep changes staged | `git reset --soft HEAD~1` | NO if pushed |
| Drop the last commit, keep changes unstaged | `git reset HEAD~1` (mixed) | NO if pushed |
| Throw away commits and edits | `git reset --hard <commit>` | NO, and destroys uncommitted work |
| Undo a commit that is already shared | `git revert <commit>` | yes, adds a new commit |
| Undo a merge commit that is shared | `git revert -m 1 <merge>` | yes, with caveat below |

`git restore` / `git switch` (Git 2.23+) split the overloaded `git checkout`. Prefer
them in scripts and docs: `git checkout -- file` and `git checkout branch` look alike and
the first one silently discards edits.

## Revert specifics
- Revert a range oldest-to-newest in one commit: `git revert --no-commit A^..B && git commit`.
- `-m 1` picks the mainline parent of a merge (parent 1 is the branch you merged INTO).
- Gotcha: after reverting a merge, re-merging the same branch later brings in only
  commits made *after* the merge; Git thinks the old ones are already there. Fix by
  reverting the revert (`git revert <revert-sha>`) before re-merging.
- Conflicts during revert: resolve, `git add`, `git revert --continue`; bail with `--abort`.

## Undoing the undo
- `reset --hard` and dropped commits: `git reflog` shows where HEAD was;
  `git reset --hard HEAD@{1}` (or the sha) brings it back. Reflog entries expire after
  90 days (30 for unreachable) by default.
- Uncommitted changes discarded by `restore` or `reset --hard` are NOT in the reflog.
  If they were ever staged, `git fsck --lost-found` can find the blobs; otherwise they
  are gone. Stash or commit first when in doubt.

## Gotchas
- `git reset <path>` (no mode) only unstages; it never touches the working tree.
- `git restore .` in a subdirectory only affects that subtree.
- `git clean -fd` removes untracked files that no undo command can recover; always run
  `git clean -nd` (dry run) first.

## Verify
- [ ] `git status` shows the expected staged/unstaged split after the command.
- [ ] For shared branches, `git log --oneline origin/main..HEAD` shows a revert commit, not a rewritten history.
- [ ] Before any `--hard`, `git stash list` / `git status` confirmed nothing uncommitted would be lost.

Related: computing-software.software-engineering.git.rebase-and-history-repair

## Checked
- Git 2.46.2: `restore`, `restore --staged`, `restore --source=HEAD~3`, `restore .` inside a subdirectory only touching that subtree, `reset --soft/mixed/--hard`, `reset <path>` only unstaging, `revert --no-commit A^..B`, revert conflict then `--abort` and `--continue`, `reset --hard HEAD@{1}` recovery, and `git fsck --lost-found` recovering a staged-then-discarded blob all behaved as written; the reflog defaults of 90 and 30 days are in the `git gc` manual; `git switch` and `restore` arrived in 2.23.
