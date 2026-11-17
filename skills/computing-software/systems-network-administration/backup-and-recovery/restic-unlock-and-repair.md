---
id: computing-software.systems-network-administration.backup-and-recovery.restic-unlock-and-repair
name: restic-unlock-and-repair
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-repair-index, restic-unlock, restic, restic-check, repository-corruption, troubleshooting]
level: advanced
status: docs-checked
description: "Fix restic repository problems: stale locks with unlock, check errors, repair index, repair snapshots and packs, and the order of operations that avoids making things worse."
sources:
  - https://restic.readthedocs.io/en/stable/077_troubleshooting.html
  - https://restic.readthedocs.io/en/stable/manual_rest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic unlock and repair

## Stale locks
"unable to create lock in backend: repository is already locked by PID ..." after a crashed
or killed run.
```sh
restic list locks
restic unlock                 # removes stale locks created by other restic processes
restic unlock --remove-all    # removes all locks, even non-stale ones: only if you're sure no other restic is running
```

## Diagnose before repairing
```sh
restic check                          # structure, index, snapshots
restic check --read-data-subset=5%    # also reads and verifies a sample of pack data
```
Back up the repository (copy at the storage level, or a storage snapshot) before repair
commands if at all possible: repairs remove data that can't be recovered.

## Repair order
Use the latest restic release, and disable `forget` and `prune` while repairing. The other steps depend on a correct index, so repair the index first.
1. **Index** problems:
   ```sh
   restic repair index         # rebuilds the index
   ```
2. **Damaged/missing pack files**: when `check` reports them it prints the exact command to run:
   ```sh
   restic repair packs <pack-id> ...   # extracts intact blobs, rebuilds the index, removes the damaged packs
   restic backup <same paths>          # re-uploads any blobs still present in the source
   ```
   If the source data still exists, a new `backup` can heal existing snapshots.
3. **Snapshots referencing missing data**:
   ```sh
   restic repair snapshots --forget    # new snapshots without damaged parts; --forget removes the originals
   restic repair snapshots --dry-run   # lists still-damaged files
   ```
4. `restic check` again until clean, then `restic prune`.

## Causes to fix
- Hardware failures, accidentally removed repository files, or restic bugs are the documented causes of damage.
- Anything other than restic deleting repository files (cleanup scripts, bucket lifecycle rules): restic must own deletion.
- `backup` and `prune` can be interrupted at any point without damaging the repository; after an interruption only `unlock` may be needed.

## Gotchas
- `repair snapshots --forget` permanently drops data references; document which files/
  snapshots were affected.

## Verify
`restic check --read-data` (full) passes on the repaired repo, and a restore test of recent
and old snapshots succeeds.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: unlock and --remove-all semantics, list locks, repair index/packs/snapshots behaviour and order, --forget and --dry-run, backup healing snapshots, interruption safety (077_troubleshooting, man pages). Removed the unconfirmed 30-minute stale-lock rule, version gates and cause list entries.

Method: documentation only; no commands were run.
