---
id: computing-software.systems-network-administration.kopia.kopia-repository-sync-and-upgrade
name: kopia-repository-sync-and-upgrade
category: computing-software
field: systems-network-administration
product: kopia
tags: [sync-to, replication, upgrade, compatibility, repository-format, disaster-recovery]
level: advanced
status: docs-checked
description: "Replicate a Kopia repository with sync-to, and plan upgrades using the compatibility promise and the v0.9 index upgrade."
sources: ["https://kopia.io/docs/advanced/synchronization/", "https://kopia.io/docs/upgrade/", "https://kopia.io/docs/advanced/compatibility/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Synchronization

`kopia repository sync-to` makes an incremental copy of the connected repository to another location, which helps disaster recovery and speeds restores from a local copy.

```console
kopia repository sync-to filesystem --path /dest/repository
kopia repository sync-to gcs --bucket my-bucket
```

You need read access to the source and read/write access to the destination. By default nothing is deleted at the destination, which stays correct but misses compaction and runs slower; add `--delete` to mirror deletions. For filesystem targets add `--must-exist` so an unmounted destination does not trigger a large re-download.

## Compatibility promise

Kopia uses semantic versioning. Since v0.3.0 each version can read snapshots from the current and at least one previous version (for v0.x, the previous minor). Older repositories are generally read-only: Kopia refuses to mutate formats it cannot safely handle, offers a migration mechanism, and never upgrades a repository format without explicit human action.

## Upgrading from v0.8 or earlier

Repositories created before v0.9 need a documented one-time upgrade to the new index format. During it no kopia instance may be connected: stop interactive CLI and KopiaUI, cron jobs, server mode under systemd, and containers. After the upgrade v0.8 and earlier cannot open the repository, and password change is available only for newly created repositories. Other upgrade paths are seamless.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Synchronization (sync-to, --delete, --must-exist), Compatibility (semantic versioning promise, read-only older formats, no automatic upgrade) and Upgrade (v0.9 index upgrade notes).
Method: documentation only; no commands were run.
