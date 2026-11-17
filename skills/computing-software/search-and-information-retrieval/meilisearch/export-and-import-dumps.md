---
id: computing-software.search-and-information-retrieval.meilisearch.export-and-import-dumps
name: export-and-import-dumps
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [dumps, import-dump, version-migration, meilisearch]
level: practitioner
status: docs-checked
description: "Create a Meilisearch dump via the dump endpoint, track the dumpCreation task, import with --import-dump, and avoid downgrades; Cloud differs."
sources: ["https://www.meilisearch.com/docs/resources/self_hosting/data_backup/dumps"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dumps

A dump is a compressed export of the whole instance, used to migrate between Meilisearch versions.

## Create (self-hosted)

Call the create-dump endpoint. It returns a summarized task with `type: dumpCreation`; fetch that task by its `taskUid` until it is `succeeded`; its `details.dumpUid` names the file. Time grows with database size. All indexes with documents and settings go into one `.dump` file in the dump directory (default `dumps`, beside where you launched). Tasks registered before processing begins are included. A visible dump file is complete: Meilisearch never leaves a partial one, even if interrupted.

The `key` field depends on the master key, so it is not propagated to dumps; a leaked dump does not expose your instance's API keys.

## Import

`./meilisearch --import-dump /dumps/20200813-042312213.dump`. The API only becomes available after the import finishes, which can take a long time. Existing indexes with the same `uid` as one in the dump are overwritten.

## Cautions

- Do not use a dump to move from a newer Meilisearch version to an older one; behaviour may be unexpected.
- Meilisearch Cloud does not let you export dumps manually; use its interface to update versions, or ask support for other needs.

## Checked

Method: docs-checked 2026-11-09 against the Exporting and importing dumps page (raw mdx of github.com/meilisearch/documentation, read in full). Replaced an unconfirmed task-polling URL with prose.
