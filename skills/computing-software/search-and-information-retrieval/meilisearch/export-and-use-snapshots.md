---
id: computing-software.search-and-information-retrieval.meilisearch.export-and-use-snapshots
name: export-and-use-snapshots
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [snapshots, schedule-snapshot, import-snapshot, meilisearch]
level: practitioner
status: docs-checked
description: "Back up a self-hosted Meilisearch with --schedule-snapshot, restore with --import-snapshot, and know the overwrite, no-migration and Cloud limits."
sources: ["https://www.meilisearch.com/docs/resources/self_hosting/data_backup/snapshots"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshots

A snapshot is an exact copy of the database: a quick backup, but not usable to migrate to a new Meilisearch release (use dumps for that). Meilisearch Cloud does not support snapshots.

## Scheduling

`meilisearch --schedule-snapshot` creates one every 24 hours, first after waiting the interval. `meilisearch --schedule-snapshot=3600` makes it hourly. Files go to the snapshot directory (default `snapshots/`) and each new one overwrites the old, so only the latest remains. For a one-off snapshot without restarting, use the `/snapshots` route.

## Restoring

`meilisearch --import-snapshot mySnapShots/data.ms.snapshot`. This is much faster than re-adding documents or importing a dump. Meilisearch never overwrites an existing database: importing into an instance holding data errors, unless you pass `--ignore-snapshot-if-db-exists=true`, in which case it starts with the existing data and ignores the snapshot.

## Checked

2026-11-03. Confirmed claim by claim against the Snapshots page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
