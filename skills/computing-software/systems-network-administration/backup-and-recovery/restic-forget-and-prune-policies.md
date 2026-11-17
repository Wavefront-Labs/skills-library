---
id: computing-software.systems-network-administration.backup-and-recovery.restic-forget-and-prune-policies
name: restic-forget-and-prune-policies
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, restic-forget, restic-prune, retention-policy, keep-daily, backup]
level: practitioner
status: docs-checked
description: "Apply restic retention with forget policies (keep-last, daily, weekly, monthly, within), grouping by host and paths, prune tuning, dry runs and lock handling."
sources:
  - https://restic.readthedocs.io/en/stable/060_forget.html
  - https://restic.readthedocs.io/en/stable/manual_rest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic forget and prune

**Goal:** keep exactly the snapshots the retention policy requires and reclaim space safely.

## forget vs prune
- `forget` removes snapshot records according to a policy (fast, metadata only).
- `prune` deletes data no longer referenced by any snapshot (reads indexes, repacks partially used packs; slower and needs an exclusive lock).
- `forget --prune` does both.

## Policies
```bash
restic forget --keep-last 3 --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 3 --dry-run
restic forget --keep-within 30d --keep-monthly 24 --prune
restic forget --tag nightly --keep-daily 14 --prune
```
- Policies apply per group; the default grouping is host and paths (`--group-by host,paths`). If paths change, a new group appears and old snapshots stay under their own group's policy. Use `--group-by host` (and the same value on `backup`) for stable grouping; `--group-by ''` applies one policy to all snapshots.
- `--keep-tag important` keeps matching snapshots; `--keep-within DURATION` keeps everything newer than the duration relative to the latest snapshot (durations like `30d`, `1y`; `1w` is not recognised).
- Calendar options (`--keep-daily` etc.) count only days/weeks/months that have at least one snapshot, on natural calendar boundaries.
- Always run `--dry-run` when changing policy.

## Prune tuning
```bash
restic prune --max-unused 5%          # default 5%; also accepts a size (200M) or unlimited
restic prune --max-repack-size 50G    # limit the total size of files repacked
restic prune --dry-run                # show what would be done
```
Repacking downloads and re-uploads data from remote repositories, so a higher `--max-unused` reduces that work; `--max-unused 0` minimises repository size. If prune fails for lack of space, run `prune --max-repack-size 0` after `forget`.

## Locks
A crashed run can leave stale locks; `restic list locks` and `restic unlock` (removes stale locks only; `--remove-all` removes all). during `prune` the repository is locked and backups cannot complete, so schedule it apart from backups.

## Append-only repositories
Clients cannot forget/prune; run retention from a trusted host with full access, and use `--keep-within` rather than count-based keep options there, because an attacker can add snapshots that push good ones out of a count-based policy.

## Verify
After forget, `restic snapshots --compact` matches the expected count per group; after prune, `restic check` passes.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: forget policy options and grouping, --keep-within durations, --max-unused (default 5%, size/percent/unlimited), --max-repack-size, prune --dry-run, max-repack-size 0 for no-free-space recovery, append-only advice to use --keep-within (060_forget).

Method: documentation only; no commands were run.
