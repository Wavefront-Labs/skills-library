---
id: computing-software.software-engineering.git.data-recovery-fsck-and-dangling-commits
name: data-recovery-fsck-and-dangling-commits
category: computing-software
field: software-engineering
product: git
tags: [git, git-internals, git-fsck, dangling-commits, data-recovery, reflog, lost-commits, corruption]
level: practitioner
status: verified
description: "Recover lost commits, stashes and staged files with reflog and fsck, and diagnose and repair repository corruption without making it worse."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
  - https://git-scm.com/docs/git-fsck
  - https://git-scm.com/docs/git-reflog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data recovery with reflog, fsck and dangling objects

**Goal:** get back work lost to a bad reset, rebase, branch deletion or dropped stash, and handle real corruption safely.

## 0. First: stop the garbage collector
Unreachable objects survive at least `gc.pruneExpire` (2 weeks by default) and reflog entries `gc.reflogExpire` (90 days) / `gc.reflogExpireUnreachable` (30 days), but do not run `git gc` or `git prune` until you have recovered. Copy the whole repo (`cp -a repo repo.bak`) before repair attempts.

## 1. Reflog (fastest path)
```bash
git reflog                       # HEAD movements
git reflog show feature-x        # a branch's history (survives until the branch is deleted)
git switch -c rescued HEAD@{5}
git reset --hard ORIG_HEAD       # undo the last reset/rebase/merge
```

## 2. Deleted branch or no reflog: fsck
```bash
git fsck --lost-found --no-reflogs     # writes dangling commits/blobs to .git/lost-found/
git fsck --unreachable | grep commit
for c in $(git fsck --no-reflogs | awk '/dangling commit/ {print $3}'); do
  git log -1 --format='%h %ci %s' $c; done
```
Branch tips that were deleted show as dangling commits; pick by date/message and `git branch rescued <sha>`.

## 3. Dropped stash
Stash commits have "WIP on" / "On <branch>" messages:
```bash
git fsck --no-reflogs | awk '/dangling commit/ {print $3}' | xargs git log --no-walk --merges --format='%h %s' | grep -E 'WIP on|On '
git stash apply <sha>
```

## 4. Staged but never committed
`git add` wrote blobs; they appear as dangling blobs:
```bash
git fsck --lost-found        # then inspect .git/lost-found/other/*
git show <blob-sha> > recovered.txt
```

## 5. Corruption
```bash
git fsck --full                  # "missing blob", "bad object", "sha1 mismatch"
```
- Re-fetch missing objects from another clone: `git fetch otherclone` or copy the specific pack.
- Replace a corrupt loose object with a good copy from a backup/clone (`.git/objects/ab/...`).
- Corrupt index: `rm .git/index && git reset`.
- Worst case: clone fresh and copy uncommitted working files over.

Run in a scratch repo: a deleted branch tip and a dropped stash both showed up as dangling commits (`WIP on master: ...`), and `git fsck --lost-found` wrote commits to `.git/lost-found/commit/` and blobs to `.git/lost-found/other/`.
## Gotchas
- `git gc --prune=now` or `git reflog expire --expire=now --all` destroys the evidence; never run them during recovery.
- Cloud-synced folders (Dropbox, OneDrive) are a common cause of corrupted `.git` directories.
- Commits pushed anywhere (forks, CI caches, PR refs) can often be fetched back by SHA.

## Verify
- `git log --oneline rescued` shows the lost work; `git fsck --full` reports no errors afterwards.
