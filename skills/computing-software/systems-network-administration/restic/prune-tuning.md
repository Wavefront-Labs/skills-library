---
id: computing-software.systems-network-administration.restic.prune-tuning
name: prune-tuning
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, prune, max-unused, max-repack-size, repack, repository-size]
level: advanced
status: docs-checked
description: "Tune restic prune with --max-unused, --max-repack-size, --repack-cacheable-only and --repack-smaller-than, and preview the plan with --dry-run."
sources:
  - https://restic.readthedocs.io/en/stable/060_forget.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customising prune

`restic prune` removes data no snapshot references. Packs that are partly used are repacked, which costs reads and writes, so prune trades time and bandwidth against wasted space.

```
restic prune --dry-run --verbose
restic prune --max-unused 10%
```

## Options

- `--max-unused limit`: tolerated unused data in the repository, as an absolute size (`200M`), a size relative to the total repository size (`10%`) or `unlimited`. Default 5%. Passing `0` minimises the space used. With `unlimited`, partly used files are left alone, but metadata is still repacked.
- `--max-repack-size size`: limit the total size of files to repack. Prune stores repacked files first and deletes the obsolete ones at the end, so this helps when you fear running low on storage.
- `--repack-cacheable-only`: when true, repack only files containing metadata that would be stored in the cache (fast, uses cached data), which can leave unused data above `--max-unused`. Default false.
- `--repack-smaller-than`: repack all pack files below this size, for example to compact packs that came from a smaller `--pack-size`.
- `--dry-run` shows only what prune would do; `--verbose` shows additional statistics.

## Choosing values

- Repacking downloads a file and re-uploads the needed data, which can be very time-consuming for remote repositories.
  `--max-unused unlimited` minimises prune time and bandwidth.
- To minimise the space used, pass `--max-unused 0`, and expect more repacking.
- If a repository is out of space, the docs suggest `prune --max-repack-size 0` (restic 0.13.0 and later) to use as
  little scratch space as possible, after first removing some snapshots with `forget`.

`forget --prune` runs prune automatically if any snapshots were actually removed. While prune runs the repository is
locked and backups cannot complete, so plan it around backup runs. It is advisable to run `restic check` afterwards.

## Checked
Compared with the "Removing backup snapshots" page: every prune option, the 5% default, the limit formats, the
`unlimited` behaviour, the lock note and the no-free-space advice. Removed: `--json` (not on the page) and the claims
that `--max-repack-size 0` means no repacking and that it spreads work across nights (the page describes it as limiting
repack size and scratch space).
Method: docs-only read of cited pages, 2026-11-08
