---
id: computing-software.software-engineering.git.undoing-merges
name: undoing-merges
category: computing-software
field: software-engineering
product: git
tags: [git, undo-merge, revert-merge, revert-mainline, reverting-a-revert, advanced-merging, merge-abort]
level: advanced
status: verified
description: "Undo a merge correctly: merge --abort mid-conflict, reset for unpushed merges, revert -m 1 for shared ones, and why re-merging later needs the revert reverted first."
sources: ["https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging", "https://git-scm.com/docs/git-revert", "https://github.com/git/git/blob/master/Documentation/howto/revert-a-faulty-merge.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undoing merges

**Goal:** back out a merge with the right tool for its state, without a later
re-merge silently dropping changes.

## State 1: merge in progress (conflicts)
```bash
git merge --abort        # restore pre-merge state (needs clean tree before merge)
git checkout --conflict=diff3 path/file   # or: redo one file's markers with base shown
git checkout --ours|--theirs path/file    # take one side for a file
```

## State 2: merge committed, not pushed
```bash
git reset --hard ORIG_HEAD     # ORIG_HEAD = tip before the merge
# or: git reset --hard HEAD~1  (first parent)
```
`--hard` discards uncommitted work too; use `--merge` / `--keep` to protect local edits.

## State 3: merge pushed / shared
```bash
git revert -m 1 <merge-sha>
```
`-m 1` = keep parent 1 (the branch you merged *into*, usually main) and undo what parent 2
brought. Check parent order with `git show --format='%P' -s <merge-sha>`.

## The trap: re-merging later
The revert undoes the *content* but Git still records the branch's commits as merged.
If the topic is fixed and merged again, only the *new* commits arrive; the originally
reverted changes stay missing.

Correct re-merge:
```bash
git revert <revert-commit-sha>    # "revert the revert" restores the original changes
git merge topic                   # now brings only the fixes
```
Alternative if the topic will be rebased anyway: rebase it with `--no-ff`/new ids
(`git rebase --no-ff main`) so its commits are new and merge normally.

## Squash or rebase merges (no merge commit)
PR merged by squash = one ordinary commit: `git revert <sha>`. Rebase-merged = several
commits: `git revert --no-commit A^..B && git commit`.

## Verify
- [ ] `git diff <merge-sha>^1 HEAD` empty for the reverted paths (content back to pre-merge).
- [ ] Re-merge plan noted in the revert commit message ("revert this revert before re-merging").

## Checked
- Git 2.46.2: `reset --hard ORIG_HEAD` returned to the pre-merge tip; `revert -m 1` removed the topic's file; a later re-merge brought only the new commit (the trap); reverting the revert and merging again restored everything; `rebase --no-ff main` gave the topic commits new ids; `git revert --no-commit A^..B && git commit` removed both commits' files; `git show --format=%P -s` listed two parents for the merge.
