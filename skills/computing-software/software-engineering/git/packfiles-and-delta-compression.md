---
id: computing-software.software-engineering.git.packfiles-and-delta-compression
name: packfiles-and-delta-compression
category: computing-software
field: software-engineering
product: git
tags: [git, packfiles, git-verify-pack, delta-compression, count-objects, repack, git-internals]
level: advanced
status: docs-checked
description: "Understand loose objects vs packfiles, inspect packs with verify-pack and count-objects, find the biggest blobs, and repack with sensible window/depth settings."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-Packfiles
  - https://git-scm.com/docs/git-verify-pack
  - https://git-scm.com/docs/git-repack
  - https://git-scm.com/docs/git-count-objects
  - https://git-scm.com/docs/git-gc
  - https://git-scm.com/docs/git-maintenance
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packfiles and delta compression

**Goal:** know where repository size comes from and how Git stores it, so you can find
the culprits and repack sensibly.

## Loose vs packed
- New objects are written **loose**: one zlib-compressed file per object under
  `.git/objects/ab/cdef...`, stored whole (no deltas).
- `git gc` (auto when there are approximately more than `gc.auto` loose objects, default
  6700) packs them into `.git/objects/pack/pack-<sha>.pack` + `.idx` (+ a `.bitmap` if
  written). A fetch or push that brings fewer than `fetch.unpackLimit` /
  `receive.unpackLimit` objects is unpacked to loose objects; larger transfers are kept as
  a pack. Inside a pack, similar objects are stored as **deltas** against a base (Pro Git's
  example stores the newer version intact and the older one as a delta, since recent
  versions are the likelier to be needed).

```bash
git count-objects -vH
# count: loose objects  size: loose size  in-pack: packed objects  size-pack: pack size  garbage: ...
```

## Inspect a pack
```bash
git verify-pack -v .git/objects/pack/pack-*.idx | sort -k3 -n -r | head
# sha type size size-in-pack offset [depth base-sha]
```
Map blob shas back to paths:
```bash
git rev-list --objects --all | grep <sha>
```
A huge blob present once in history keeps costing every clone; remove it with
filter-repo (see removing sensitive data skill) and move such files to LFS.

## Repacking
```bash
git repack -a -d                       # one pack, drop redundant packs
git repack -a -d -f --depth=50 --window=250   # -f recomputes deltas instead of reusing (slow)
git gc --aggressive                    # optimises harder at the cost of much more time
git repack -a -d --write-bitmap-index  # faster clones/fetches for servers
```
`--window` = how many candidate objects to compare; `--depth` = max delta chain length
(longer = smaller but slower reads). Defaults are `--window=10` and `--depth=50` (the maximum depth is 4095).

## Gotchas
- Binary files that change wholly (zip, images, compressed assets) delta poorly; size grows
  per version. Use LFS.
- A `.keep` file next to a pack keeps its objects out of repacking unless
  `--pack-kept-objects` is given, and `.keep` packs are not deleted.
- Multiple packs are normal; the `incremental-repack` maintenance task (daily in the
  `git maintenance start` schedule) consolidates them gradually.

## Verify
- [ ] `git count-objects -vH` reports `garbage: 0` and modest loose count.
- [ ] Largest blobs list contains nothing that should be in LFS or not in Git at all.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Pro Git packfiles chapter. Confirmed: `gc.auto` default 6700; `fetch.unpackLimit` / `receive.unpackLimit` behaviour; `git count-objects -v` fields (count, size, in-pack, size-pack, garbage); `git verify-pack -v` columns (object-name, type, size, size-in-packfile, offset); `git repack` options `-a -d -f --window --depth --write-bitmap-index` with defaults window 10 and depth 50, maximum depth 4095; `.keep` handling and `--pack-kept-objects`; `incremental-repack` is a daily maintenance task; Pro Git states the newest version is stored intact. Removed as unconfirmed: the `.rev` file mention and the thin-pack remark.

Method: documentation only; no commands were run.
