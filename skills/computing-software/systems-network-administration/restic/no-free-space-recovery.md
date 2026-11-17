---
id: computing-software.systems-network-administration.restic.no-free-space-recovery
name: no-free-space-recovery
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, prune, no-free-space, recovery, unsafe-recover-no-free-space]
level: sme
status: docs-checked
description: "Recover a full restic repository using forget, prune --max-repack-size 0 and, as a last resort, prune --unsafe-recover-no-free-space, then repair the index."
sources:
  - https://restic.readthedocs.io/en/stable/060_forget.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering from "no free space"

When the repository's storage is full, prune itself may fail because it needs temporary space to repack.

## Step 1: free space without repacking

Remove snapshots, then prune without repacking:

```
restic forget <snapshot-ID>
restic prune --max-repack-size 0
```

`--max-repack-size 0` makes prune use as little scratch space as possible; it only helps if snapshots were already removed with `forget`. For restic versions before 0.13.0 use `--max-repack-size 1`. If it succeeds but space is still low, forget a few more snapshots and prune again. Run `restic check` after pruning.

## Step 2: last resort

If even that is not possible, the docs describe `--unsafe-recover-no-free-space`. It is a two-step command: first run it with the placeholder `SOME-ID`:

```
restic prune --unsafe-recover-no-free-space SOME-ID
```

The first run does not proceed; rerun with `SOME-ID` replaced by the ID it requests. A failed run can leave the repository temporarily unusable, so make sure you have a stable connection to the storage first.

## After an unsafe prune

If the command fails, it may be necessary to manually remove all files from the repository's `index/` folder and then run `restic repair index`. Then run `restic check` and, if needed, repair damaged snapshots (see repair-damaged-repo).

## Prevent it

Monitor free space on the backend: prune needs some scratch space to work, and repacking downloads and re-uploads partly used pack files.

## Checked

Checked 2026-11-08 against the restic Removing backup snapshots page (060_forget), read in full. Confirmed: prune needing scratch space, prune --max-repack-size 0 (1 before 0.13.0), the forget-first requirement, --unsafe-recover-no-free-space SOME-ID two-step use, the risk of an unusable repository, and clearing index/ then restic repair index. Removed: the claim that max-repack-size 0 writes no new packs, which the page does not state in that form.

Method: documentation only; no commands were run.
