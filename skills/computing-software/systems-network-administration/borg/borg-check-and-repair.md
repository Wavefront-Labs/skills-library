---
id: computing-software.systems-network-administration.borg.borg-check-and-repair
name: borg-check-and-repair
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-check, verify-data, repair, repository-check, max-duration, zero-patched]
level: advanced
status: docs-checked
description: "Verify Borg repository integrity with borg check: repository versus archive steps, verify-data, partial max-duration checks, and the data-loss risks of repair."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/check.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg check and repair

`borg check` runs two steps. Repository check validates segment headers and every object's size and CRC; archive check validates archive metadata and file chunk lists. Cryptographic verification only happens with `--verify-data` (reads, decrypts and decompresses everything; very slow, conflicts with `--repository-only`).

Options: `--repository-only`, `--archives-only`, `--repair`, `--save-space`, `--max-duration SECONDS`, archive filters `-a GLOB`, `--first/--last N`, `--sort-by`.

Partial checks: `--max-duration` does only non-cryptographic segment checksum checks over a time slice. It requires `--repository-only` and cannot be combined with `--archives-only` or `--repair`. A full repository check aborts any previous partial check.

On a remote repository, the repository check runs on the server, the archive check on the client (it needs the key).

Without `--repair` the check is read-only. The docs call `--repair` potentially dangerous: back up the repository first, and stress-test disk and RAM beforehand. Repair may recover objects from damaged segments, drop archives whose metadata chunk is lost, replace lost file chunks with same-size all-zero chunks (zero-patched files), and delete orphaned chunks. `extract` warns on zero-patched files; `mount` returns EIO unless `-o allow_damaged_files`. If the lost chunks reappear in later backups, run `--repair` again to heal. Automate the confirmation with `BORG_CHECK_I_KNOW_WHAT_I_AM_DOING=YES`.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/check): check options, partial-check limits, repair behaviour and zero-patched files (check page), allow_damaged_files/EIO (mount page), BORG_CHECK_I_KNOW_WHAT_I_AM_DOING (General page). Removed: nothing.

Method: documentation only; no commands were run.
