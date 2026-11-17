---
id: computing-software.software-engineering.git.repairing-repository-corruption
name: repairing-repository-corruption
category: computing-software
field: software-engineering
product: git
tags: [git, repository-corruption, corrupt-index, missing-objects, broken-refs, git-fsck, object-file-is-empty]
level: advanced
status: docs-checked
description: "Recover a corrupted repo: 'object file is empty', bad index, broken or empty refs, missing objects. Back up, run fsck, restore objects from a clone, rebuild index and refs."
sources:
  - https://git-scm.com/docs/git-fsck
  - https://git-scm.com/docs/howto/recover-corrupted-blob-object
  - https://git-scm.com/docs/howto/recover-corrupted-object-harder
  - https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
  - https://git-scm.com/docs/git-reset
  - https://git-scm.com/docs/git-gc
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing repository corruption

**Goal:** get a working repository back after a crash, full disk, sync tool (Dropbox,
OneDrive) or bad hardware damaged `.git`, losing as little as possible.

## 0. Stop and back up
```bash
cp -a myrepo myrepo-backup        # including .git; never experiment on the only copy
```
If a remote has everything you pushed, the easy fix is a fresh clone plus copying over
uncommitted files. Do the steps below only for unpushed work.

## 1. Find the damage
```bash
git fsck --full --no-dangling
```
Typical messages and fixes:

### "error: object file .git/objects/ab/cd... is empty" / "loose object is corrupt"
Crash while writing (common on VMs and synced folders).
```bash
mv .git/objects/<xx>/<rest-of-sha> ../          # move the bad object file out of the way, do not delete it yet
git fsck --full                       # now reports it as missing
git fetch origin                      # recovers anything that exists remotely
```
For a single missing blob you still have on disk: `git hash-object -w path/to/file`
recreates it if the content matches (the git howto on recovering a corrupted blob object
walks through this, using `git log --raw --all --full-history -- <path>` to find the file's
history).

### "index file corrupt"
```bash
rm .git/index
git reset                 # rebuild index from HEAD; working tree untouched (mixed)
```

### Broken or empty ref ("fatal: bad object HEAD", "ref ... is empty")
```bash
cat .git/HEAD                         # should be "ref: refs/heads/main"
git reflog show main | head           # or read .git/logs/refs/heads/main for the last sha
git update-ref refs/heads/main <last-good-sha>
```
If `.git/HEAD` itself is garbage: `git symbolic-ref HEAD refs/heads/main`.

### Missing objects that no remote has
Find what references them (`git fsck` names the tree/commit), recover file contents from
the working tree or backups, and as a last resort rewrite history to drop the broken
commit (re-create it from the working tree).

## 2. Confirm and harden
```bash
git fsck --full && git gc --prune=now
```
Prevent recurrence: do not keep repos inside cloud-sync folders; set `core.fsync=committed`
(Git 2.36+) on unreliable storage; enable `transfer.fsckObjects` to catch bad objects on fetch.

## Verify
- [ ] `git fsck --full` prints no errors.
- [ ] `git log --all --oneline | head` and `git status` work; unpushed commits present.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed: `git fsck --full` and `--no-dangling`; the howto recipe of moving a corrupt loose object aside and recreating it with `git hash-object -w`; `git update-ref`, `git symbolic-ref HEAD`; `git reset` (mixed by default, rebuilds the index without touching the working tree); `git gc --prune=now`; `core.fsync` with the `committed` aggregate (Git 2.36 release notes); `transfer.fsckObjects` (default false). Removed as unconfirmed: the blanket deletion of empty object files, the copy-packs-from-another-clone step, the exact `bad signature` message and the hand-written `.git/HEAD` echo.

Method: documentation only; no commands were run.
