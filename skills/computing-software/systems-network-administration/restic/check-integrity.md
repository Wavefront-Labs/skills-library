---
id: computing-software.systems-network-administration.restic.check-integrity
name: check-integrity
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, check, read-data, read-data-subset, integrity, verification]
level: practitioner
status: docs-checked
description: "Verify a restic repository with restic check, including --read-data, --read-data-subset by fraction, percentage or size, and --with-cache."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
  - https://restic.readthedocs.io/en/stable/077_troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking a repository

```
restic -r /srv/restic-repo check
```

The plain check verifies repository structure and consistency but does not read every pack file. The docs advise running it regularly and after pruning.

## Reading data

- `--read-data` reads and verifies every pack file; it can cost more bandwidth and time than a default check.
- `--read-data-subset=n/t` checks one of `t` groups, e.g. `1/10`, then `2/10` on later days to cover everything over time.
- `--read-data-subset=x%` checks a percentage, e.g. `5%`.
- `--read-data-subset=nS` checks a random subset of about `n` bytes of pack files, with unit K, M, G or T (converted to a percentage of the repository size).

## Cache

`--with-cache` reuses the existing cache. By default check creates a new temporary cache directory.

## Errors

If check reports problems, it suggests commands. Typical suggestions are `restic repair index`, `restic repair packs`, `restic repair snapshots --forget` and `restic prune`. Before repairing, copy the whole repository if you can, or at least the `index` and `snapshots` folders, and keep the original check output. Use `restic repair packs` instead of repairing the index when check tells you to.

Warnings that ciphertext verification failed are often caused by hardware problems that must be investigated and fixed.

Include `restic check` in scheduled jobs and alert when it reports errors.

## Checked

Checked 2026-11-08 against the restic Working with repositories page (045_working_with_repos) and Troubleshooting page (077_troubleshooting), both read in full. Confirmed: check, --read-data, the three --read-data-subset forms, --with-cache and the default temporary cache, the repair suggestions, backing up index and snapshots folders, keeping check output, and the ciphertext warning. Removed: the claim that plain check is cheap enough after each backup, the stale-cache rationale and the non-zero exit-code remark.

Method: documentation only; no commands were run.
