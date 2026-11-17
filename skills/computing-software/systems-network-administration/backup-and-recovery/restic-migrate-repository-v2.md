---
id: computing-software.systems-network-administration.backup-and-recovery.restic-migrate-repository-v2
name: restic-migrate-repository-v2
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-migrate, restic, repository-v2, restic-compression, repository-upgrade, restic-prune]
level: practitioner
status: docs-checked
description: "Upgrade a restic repository from format v1 to v2 to enable compression: pre-checks, migrate upgrade_repo_v2, repacking old data, and client version compatibility."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html#upgrading-the-repository-format-version
  - https://restic.readthedocs.io/en/stable/077_troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading a restic repository to format v2

**Goal:** enable compression on an old repository without risking the data.

## Before
1. Every client and script touching the repo must run restic **0.14.0 or newer**; older versions cannot read v2.
2. Take a copy if the repo is the only one (or `restic copy` to a new v2 repo instead of in-place migration).
3. Repository problems must be corrected first: the migration runs an integrity check and will not proceed otherwise. Stop all backups while migrating.

## Migrate
```sh
restic migrate                       # lists available migrations
restic migrate upgrade_repo_v2       # checks repository integrity, then upgrades the version
```
Existing file contents are not rewritten; data from new backups is compressed (`--compression auto` by default). Afterwards run `restic prune` to compress the repository metadata.

## Compress existing data (optional)
```sh
restic prune --repack-uncompressed               # rewrites all uncompressed packs
restic prune --repack-uncompressed --max-repack-size 200G   # in stages
```
Repacking reads and rewrites the whole repo: plan for time, temporary extra space, and cloud egress/requests. Skip it for already-compressed data.

## Check
`restic cat config` shows `"version": 2` (the config JSON carries the repository format version). `restic stats --mode raw-data` drops after repacking.

## Gotchas
- Upgrading raises the minimum restic version needed to access the repository (0.14.0 for v2), so old restic binaries on forgotten hosts (NAS cron jobs, container images) can no longer use it; inventory them first.
- The compression level of data already stored cannot be changed later, so add `--compression max` to the repack `prune` if you want maximum compression.
- `prune` can be interrupted at any point without damaging the repository; run `restic check` afterwards.

## Verify
`restic check --read-data-subset=5%` passes after migration and a restore of an old snapshot works.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: v2 needs restic 0.14.0+, v2 is the default for new repositories (030), migrate upgrade_repo_v2 flow, prune --repack-uncompressed and --max-repack-size, no rewrite of existing contents (045_working_with_repos).

Method: documentation only; no commands were run.
