---
id: computing-software.systems-network-administration.backup-and-recovery.restic-repository-checks
name: restic-repository-checks
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, restic-check, read-data-subset, repository-integrity, restic-repair, backup-verification]
level: practitioner
status: docs-checked
description: "Verify restic repository integrity: structural checks, rotating read-data-subset verification of pack contents, cache options, and repair commands when problems appear."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
  - https://restic.readthedocs.io/en/stable/077_troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic repository checks

**Goal:** detect corruption or missing data in a restic repository before you need a restore.

## Structural check
```bash
restic check
```
Verifies the structural consistency and integrity of snapshots, trees and pack files. The restic manual advises running it after pruning.

## Data verification
```bash
restic check --read-data                    # reads and verifies every pack: full download on cloud backends
restic check --read-data-subset=1/12        # one twelfth of packs, chosen deterministically
restic check --read-data-subset=5%          # random 5%
restic check --read-data-subset=20G         # random subset of about 20 GiB (k/K, m/M, g/G, t/T suffixes)
```
With `n/t`, run n = 1..t in turn (for example 1/5 to 5/5, one per run) so every pack is read once per cycle; `x%` and size subsets are random and give no coverage guarantee.

## Cache
By default `check` creates a new temporary cache directory; `--with-cache` reuses the existing cache and only reads uncached data from the repository.

## When check fails
- Missing packs or damaged blobs: identify affected snapshots (output names them); `restic repair index` rebuilds the index from packs; `restic repair snapshots --forget` rewrites snapshots without damaged files and removes the originals (repairing and deleting broken snapshots causes data loss; if the source files still exist, a new `backup` can heal existing snapshots instead). Run `repair index` first: the other repair steps depend on a correct index.
- Then run a new backup so affected files are stored again.
- Investigate the backend (disk errors, interrupted uploads, bucket lifecycle rules deleting objects).

## Gotchas
- Restic does not natively support cold storage (experimental S3 Glacier restore exists); do not transition repository objects to archive tiers.
- `--read-data` downloads every pack from remote backends; subsets spread the cost.
- When `check` reports damaged packs or snapshots it prints the matching `repair packs` or `repair snapshots` command; follow that output.

## Verify
Check job logs show "no errors were found" and the subset rotation completes a full cycle in the planned period.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: check flags (--read-data, --read-data-subset n/t, x%, size with suffixes, --with-cache and the temporary-cache default), repair index before other repairs, repair snapshots --forget semantics, cold storage statement (faq), check after prune advice (060_forget, 077_troubleshooting, man pages).

Method: documentation only; no commands were run.
