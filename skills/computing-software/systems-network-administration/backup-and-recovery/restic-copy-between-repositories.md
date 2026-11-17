---
id: computing-software.systems-network-administration.backup-and-recovery.restic-copy-between-repositories
name: restic-copy-between-repositories
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-copy, restic, offsite-copy, 3-2-1, repository-replication, chunker-params]
level: practitioner
status: docs-checked
description: "Copy restic snapshots between repositories for offsite copies: from-repo options, matching chunker parameters for dedup, filters, scheduling, and verifying the copy."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html#copying-snapshots-between-repositories
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying snapshots between restic repositories

**Goal:** a second, independent repository (other site/cloud, other credentials) holding copies of your snapshots, for 3-2-1.

## Create the destination with the same chunker
`copy` does not re-chunk files, so deduplication against data already in the destination only works when both repositories use the same chunker parameters. Initialise the target copying them:
```sh
restic -r s3:s3.eu-west-2.amazonaws.com/acme-restic-offsite init \
  --from-repo /srv/restic-local --from-password-file /root/.restic-local-pw --copy-chunker-params
```
Without `--copy-chunker-params`, copy still works, but files present in both repositories may occupy up to twice their space in the destination.

## Copy
```sh
export RESTIC_REPOSITORY=s3:s3.eu-west-2.amazonaws.com/acme-restic-offsite
export RESTIC_PASSWORD_FILE=/root/.restic-offsite-pw
restic copy --from-repo /srv/restic-local --from-password-file /root/.restic-local-pw
restic copy --from-repo /srv/restic-local --from-password-file /root/.restic-local-pw --host db01 --tag daily
restic copy ... 4f2a1c9b latest              # specific snapshots (IDs or latest)
```
The source can also come from `--from-repository-file` or `RESTIC_FROM_REPOSITORY` / `RESTIC_FROM_PASSWORD_FILE` / `RESTIC_FROM_PASSWORD_COMMAND`. Filters are `--host`, `--path` and `--tag`.
Snapshots that were already copied are skipped by later runs (shown only with `--verbose`), so run it after every backup.

## Retention on each side
Run `forget --prune` independently on each repository; the offsite copy can keep longer history (e.g. local 14 dailies, offsite 12 monthlies).

## Scheduling
Run `copy` after the backup job (for example a second systemd unit ordered `After=` the backup unit), and `check --read-data-subset` on the target on a schedule.

## Gotchas
- Different passwords per repo are normal and recommended; keep both in the vault.
- Copying from a corrupt source copies the damage; run `restic check` on the source first.
- Copy downloads and re-uploads the whole snapshot data because the two repositories use different encryption keys: expect higher bandwidth and cost than a normal backup, including egress if the source is in the cloud.

## Verify
`restic snapshots` on both repos shows the same snapshot set (snapshot IDs may differ between repositories); restore a file from the offsite copy.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: init --from-repo --copy-chunker-params, copy flags (--from-repo, --from-password-file, --from-repository-file, --host, --path, --tag), skipping of already-copied snapshots, no re-chunking, full download and upload because of different keys. Corrected the claim that copy re-splits chunks, and removed the unverifiable note about old --repo2 syntax.

Method: documentation only; no commands were run.
