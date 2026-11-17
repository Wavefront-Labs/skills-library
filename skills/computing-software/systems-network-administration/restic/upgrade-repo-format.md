---
id: computing-software.systems-network-administration.restic.upgrade-repo-format
name: upgrade-repo-format
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, migrate, upgrade-repo-v2, compression, repository-version]
level: advanced
status: docs-checked
description: "Upgrade a restic repository from format version 1 to 2 with restic migrate upgrade_repo_v2, then recompress old data with prune."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading to repository format 2

Format 2 adds compression and requires restic 0.14.0 or newer on every client.

```
restic -r /srv/restic-repo migrate upgrade_repo_v2
```

The upgrade is a two-step process: `migrate upgrade_repo_v2` checks repository integrity and then upgrades the version; repository problems must be fixed first. Afterwards run `prune` to compress the repository metadata. File contents already stored are not rewritten, so the repository does not shrink yet.

## Compress old data

New backups are compressed. To recompress existing packs, run a prune that repacks uncompressed data:

```
restic prune --repack-uncompressed
restic prune --repack-uncompressed --compression max
restic prune --repack-uncompressed --max-repack-size 20G
```

`--max-repack-size` limits the total size of files to repack. Adding `--compression max` is for when you plan maximum compression; the level of already backed up data cannot be changed later.

## Compression mode

Choose with `--compression` or `RESTIC_COMPRESSION`: `off`, `fastest`, `auto` (default), `better` or `max`. It only applies to format version 2.

## Checked

2026-11-03. Confirmed in the restic docs pages Working with repositories (Upgrading repository version), Preparing a new repository (version table) and Removing backup snapshots (`--max-repack-size`), and Tuning parameters (compression values and default): the migrate command, the prune follow-up, `--repack-uncompressed`, `--max-repack-size`, compression modes. Removed: the claims that the migration only changes configuration, the cloud-transfer note and the advice to run `restic check` (not in the docs).

Method: documentation only; no commands were run.
