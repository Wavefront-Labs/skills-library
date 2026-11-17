---
id: computing-software.systems-network-administration.restic.repair-damaged-repo
name: repair-damaged-repo
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, repair, troubleshooting, repair-index, repair-snapshots, repair-packs]
level: sme
status: docs-checked
description: "Follow the restic troubleshooting sequence for a damaged repository: check --read-data, back up index and snapshots, repair index, repair snapshots, rerun backups."
sources:
  - https://restic.readthedocs.io/en/stable/077_troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing a damaged repository

Use the latest restic; it may contain fixes. Follow these steps in order.

1. **Find the damage.** `restic check --read-data` and keep a copy of the output (it downloads the whole repository, so omit `--read-data` if that is expensive). Warnings that ciphertext verification failed are often caused by hardware problems that must be fixed first. If check reports damaged pack files it shows how to repair them with `restic repair packs`; use that instead of the index step below.
2. **Copy the repository**, or at least its `index` and `snapshots` folders (rclone can copy cloud storage), and disable all regular operations, especially `forget` and `prune`.
3. **Repair the index** with `restic repair index`, which removes no-longer-existing pack files from the index. It is not recommended unless the repository is actually damaged, and later repair steps rely on a correct index, so do it first.
4. **Rerun all backups (optional).** With a correct index, new snapshots are guaranteed restorable and may heal older snapshots; run `restic check` again afterwards. `restic repair snapshots --dry-run` lists still-damaged snapshots (look for "would save new snapshot").
5. **Remove missing data from snapshots** if data is still missing: `restic repair snapshots --forget` removes inaccessible data from snapshots (a limited data loss) and removes the damaged originals. Without `--forget`, run `restic forget <id>` on each modified snapshot.
6. **Final check.** `restic check --read-data` should report no errors were found; if not, ask for help on the restic forum or IRC channel.

Backup and prune can be interrupted at any point without damaging the repository, but you might have to run `restic unlock` manually.

## Checked

Checked 2026-11-08 against the restic Troubleshooting page (077_troubleshooting), read in full. Confirmed: use the latest restic, the check --read-data first step and keeping its output, the ciphertext warning, repair packs preference, copying index and snapshots folders and rclone, disabling forget and prune, repair index and its ordering, rerunning backups, repair snapshots --dry-run and --forget, final check, and manual unlock. Reordered the steps to follow the page; removed the instruction to run repair snapshots on a given snapshot ID only when check says so, which the page does not state.

Method: documentation only; no commands were run.
