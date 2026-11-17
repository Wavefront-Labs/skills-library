---
id: computing-software.software-engineering.git.merge-strategies-and-options
name: merge-strategies-and-options
category: computing-software
field: software-engineering
product: git
tags: [git, git-merge, merge-strategies, merge-strategy-ort, strategy-option-theirs, ours-strategy, octopus, ignore-space-change, renormalize]
level: advanced
status: verified
description: "Choose Git merge strategies and -X options: ort defaults, -X ours/theirs vs -s ours, whitespace and renormalize options, octopus and subtree merges."
sources: ["https://git-scm.com/docs/merge-strategies", "https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging", "https://git-scm.com/docs/git-merge"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merge strategies and strategy options

**Goal:** steer a merge when the default result is wrong or noisy, without accidentally
discarding the other side's work.

## Strategies (`-s`)
| Strategy | Use |
|---|---|
| `ort` | Default since Git 2.34 for two heads. Faster than old `recursive`, better rename handling. |
| `recursive` | Legacy; same options as ort. Only if you hit an ort edge case. |
| `octopus` | Default for 3+ branches; refuses if any manual conflict. Good for many independent topic branches. |
| `ours` | Records a merge but keeps OUR tree entirely; the other side's changes are discarded. Used to mark an old branch as "merged" (superseded). |
| `subtree` | Merge a project into a subdirectory (see git-subtree skill). |

## Strategy options (`-X`) for ort/recursive
```bash
git merge -X theirs feature          # in CONFLICTING hunks, prefer theirs; non-conflicting changes from both kept
git merge -X ours feature            # in conflicting hunks, prefer ours
git merge -X ignore-space-change     # treat whitespace-only changes as unchanged
git merge -X ignore-all-space
git merge -X renormalize             # run line-ending/attribute normalization before 3-way merge
git merge -X find-renames=40%        # rename detection threshold (default 50%)
git merge -X diff-algorithm=histogram
```
The classic mistake: `-s ours` and `-X ours` are completely different. `-X ours` still
takes every non-conflicting change from the other branch; `-s ours` takes none of them.

## Resolving per-file during a conflict
```bash
git checkout --ours  path/file      # (or git restore --ours) take our version wholesale
git checkout --theirs path/file
git checkout -m path/file           # recreate conflict markers if you botched a resolution
git merge --abort                   # back to pre-merge state
```
During a REBASE, "ours" is the branch being rebased onto (upstream) and "theirs" is your
commit being replayed; the labels flip compared with merge.

## Previewing a merge without touching the worktree
```bash
git merge-tree --write-tree main feature   # Git 2.38+: prints tree id; exit 1 if conflicts
```
Useful in CI or bots to test mergeability.

## Verify
- [ ] After `-X theirs/ours`, ran the tests: auto-chosen hunks can be syntactically fine but semantically wrong.
- [ ] `git log --merges -1 --stat` shows the expected files changed.
- [ ] Never used `-s ours` unless the intent was to discard the other branch.

## Checked
- Git 2.46.2 in scratch repos: two heads merge with `ort`, three heads with `octopus`; an octopus merge whose heads touch the same file stops with `content conflict` / `merge program failed` and `merge --abort` restores the tree; `-s ours` kept none of the topic's changes while `-X ours` kept its non-conflicting file and `-X theirs` took the topic's conflicting line but kept our non-conflicting one; `checkout --ours/--theirs`, `checkout -m` and `--conflict=diff3` behave as written; during a rebase `--ours` was the branch rebased onto; `git merge-tree --write-tree` printed a tree id and exited 1 on a conflict (with conflicted-file lines) and 0 when clean; `-X renormalize`, `diff-algorithm=histogram`, `find-renames=40%`, `ignore-all-space`, `no-renames` are accepted. The 2.34.0 release notes make `ort` the default and 2.38.0 adds the merge-tree mode; the `git merge` manual lists octopus for several heads. The 50% rename threshold and ignore-space result were not exercised.
