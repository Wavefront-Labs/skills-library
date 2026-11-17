---
id: computing-software.software-engineering.git.rebase-onto-transplanting-commits
name: rebase-onto-transplanting-commits
category: computing-software
field: software-engineering
product: git
tags: [git, rebase-onto, git-rebase, transplant-commits, dependent-branches, fork-point]
level: advanced
status: verified
description: "Move a range of commits to a new base with git rebase --onto: detach a stacked branch, drop commits from the middle, and recover after a parent squash-merge."
sources: ["https://git-scm.com/book/en/v2/Git-Branching-Rebasing", "https://git-scm.com/docs/git-rebase", "https://git-scm.com/docs/git-merge-base#_discussion_on_fork_point_mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transplanting commits with rebase --onto

**Goal:** replay exactly the commits you mean onto a new base, instead of everything
`git rebase <upstream>` would pick.

## The three-argument form
```
git rebase --onto <newbase> <upstream> [<branch>]
```
Takes commits in `<upstream>..<branch>` (reachable from branch, not from upstream) and
replays them on `<newbase>`. Read it as "onto NEWBASE, the commits after UPSTREAM, of BRANCH".

## Recipes
**Branch built on a feature branch, feature not merged yet; you want it off main:**
```bash
#   main -- A -- B (featureA) -- C -- D (featureB)
git rebase --onto main featureA featureB
#   main -- C' -- D' (featureB)
```

**Parent branch was squash-merged into main** (featureB still contains A, B):
```bash
git rebase --onto origin/main featureA featureB
# if featureA was already deleted, use the old tip sha (from reflog or PR page)
git rebase --onto origin/main <old-featureA-sha> featureB
```
Plain `git rebase origin/main` would try to replay A and B again and conflict, because
the squash commit has a different patch identity.

**Drop commits in the middle** (remove C and D, keep E, F):
```bash
#   ... B -- C -- D -- E -- F (topic)
git rebase --onto B D topic
```

**Last N commits onto another branch:**
```bash
git rebase --onto release-1.4 HEAD~3
```

## Fork-point and its surprises
`git rebase` without an explicit upstream uses `--fork-point` with the reflog of the
upstream, which can silently drop commits that upstream once contained (e.g. after
upstream was force-pushed). When the result looks wrong, pass explicit arguments
or `--no-fork-point`.

## Safety
- Rebasing rewrites hashes: only for unshared branches or with team agreement, then
  `git push --force-with-lease`.
- Before a tricky transplant: `git branch backup/featureB` (or rely on `ORIG_HEAD` / reflog).
- Stacked branches: `git rebase --update-refs` moves intermediate branch pointers too.
- Inspect the range first: `git log --oneline <upstream>..<branch>` is exactly what moves.

## Verify
- [ ] `git log --oneline <newbase>..<branch>` lists only intended commits.
- [ ] `git range-diff <upstream>..<backup> <newbase>..<branch>` shows patches unchanged.

## Checked
- Git 2.46.2: `rebase --onto main featureA featureB` moved only B1 and B2; with a squash-merged parent a plain `rebase main` hit a conflict while `--onto origin/main featureA featureB` replayed only B1; the `<old-sha>` form works after the parent branch is deleted; `--onto B D topic` dropped C and D and kept E and F; `--onto release-1.4 HEAD~3` selects the last three; after an upstream force-push the default fork-point `git rebase` dropped the commit upstream once had (`T1 U2 base`) while `--no-fork-point` kept it (`T1 U1 U2 base`); `--update-refs` moved the intermediate branch.
