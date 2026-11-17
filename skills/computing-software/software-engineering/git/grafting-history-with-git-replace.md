---
id: computing-software.software-engineering.git.grafting-history-with-git-replace
name: grafting-history-with-git-replace
category: computing-software
field: software-engineering
product: git
tags: [git, git-replace, graft, history-truncation, join-histories, refs-replace]
level: advanced
status: verified
description: "Use git replace to graft separate histories together or truncate a huge history for daily use, share replacement refs, and make grafts permanent with filter-repo."
sources: ["https://git-scm.com/book/en/v2/Git-Tools-Replace", "https://git-scm.com/docs/git-replace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafting history with git replace

**Goal:** make Git treat one object as another, e.g. attach an old imported history to
a fresh repo, or give a short "recent" repo with the full history available on demand.

## How it works
`git replace <object> <replacement>` writes `refs/replace/<object-sha>` pointing at the
replacement. Almost every command (log, blame, checkout) then transparently uses the
replacement. Hashes of existing commits do not change.

## Joining two histories (graft)
Situation: `new` repo started from a snapshot; `old` repo holds years of history ending
in the same tree.
```bash
git remote add old ../old-repo && git fetch old
# first commit of the new history, last commit of the old one:
FIRST=$(git rev-list --max-parents=0 main)
git replace --graft $FIRST old/main
git log --oneline | tail     # now continues into old history
```
`--graft <commit> [<parent>...]` creates a copy of the commit with new parents and replaces it.

## Truncating for a lightweight repo (Pro Git recipe)
Keep recent history in a small repo; replace its root with a commit pointing at the
archived history only for people who fetch it.

## Sharing replacements
Not transferred by default:
```bash
git push origin 'refs/replace/*'
git fetch origin 'refs/replace/*:refs/replace/*'
```
Disable temporarily: `git --no-replace-objects log` or `GIT_NO_REPLACE_OBJECTS=1`.

## Making it permanent
Hosts, CI and fresh clones ignore replace refs unless fetched. For a permanent join,
rewrite: `git filter-repo --force --proceed` (no filters; the rewrite reads through the replace
refs, so the graft becomes real parentage; tested: 5 commits afterwards with `--no-replace-objects` and no `refs/replace`), then everyone re-clones. A fresh clone needs no `--force`. Check the result with
`git --no-replace-objects log` before pushing.

## Managing
```bash
git replace -l              # list
git replace -d <sha>        # delete
git replace --edit <sha>    # edit an object's raw content in $EDITOR
```

## Gotchas
- `git fsck` and `gc` honour replacements; objects reachable only through the original may be pruned
  once nothing references them.
- Shallow clones and replace refs interact badly; use one mechanism.

## Verify
- [ ] `git log --oneline --graph` shows continuous history across the graft point.
- [ ] Team knows to fetch `refs/replace/*` or the graft was made permanent.
