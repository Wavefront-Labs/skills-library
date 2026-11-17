---
id: computing-software.ai-ml-engineering.mastra.eval-datasets
name: eval-datasets
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, dataset, experiment, evals, versioning, schemas, snapshot, purge]
level: practitioner
status: docs-checked
description: "Create versioned Mastra datasets, enforce input and groundTruth schemas, add, update, purge and list items, pin versions and validate portable snapshot artifacts."
sources:
  - https://mastra.ai/docs/evals/datasets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep reproducible test cases for experiments. Added in `@mastra/core@1.4.0`. Every mutation creates a new dataset version.

## Setup
Storage must provide the `datasets` domain, e.g. `new Mastra({ storage: new LibSQLStore({ id: 'my-store', url: 'file:./mastra.db' }) })`. Operations live on `mastra.datasets` (`create`, `get({ id })`, `list()`). Studio (Datasets in the sidebar) offers the same, plus CSV/JSON import with column mapping and a version diff.

## Create with schemas
```typescript
const dataset = await mastra.datasets.create({
  name: 'translation-pairs',
  description: 'English to Spanish translation test cases',
  inputSchema: z.object({ text: z.string(), sourceLang: z.string(), targetLang: z.string() }),
  groundTruthSchema: z.object({ translation: z.string() }),
})
```
Any Standard JSON Schema library works (Zod, Valibot, ArkType). Non-matching items are rejected at insert.

## Items
```typescript
await dataset.addItem({ input: {...}, groundTruth: {...} })
await dataset.addItems({ items: [ {...}, {...} ] })
await dataset.updateItem({ itemId, groundTruth: {...} })
await dataset.deleteItem({ itemId })            // also deleteItems({ itemIds })
await dataset.purgeItem({ itemId })
const { items, pagination } = await dataset.listItems({ page: 0, perPage: 50, search: 'Hello', version: 2 })
```
- Delete hides the item from the current version but history keeps its content. `purgeItem` redacts content across history and linked experiment results, creates no version, cannot be undone, and keeps identity and counters. A concurrent `updateItem` can reject with `DATASET_ITEM_PURGED`. MongoDB purge needs a replica set or sharded deployment with transactions. Do not put sensitive data in `externalId`.
- Config updates: `null` clears schemas, tags, target type/ids, scorer IDs. Item `scorerIds: null` removes the override; `[]` disables scoring for that item.
- Retrying with the same `externalId` returns the original item; omitted and `null` payload fields are treated the same on retry.
- `listItems({ version })` without `search`/`page`/`perPage` returns a bare array (deprecated); pass `page` and `perPage`.

## Versions
Add, update and delete bump the version. `listVersions()`, `getItemHistory({ itemId })`, and `listItems({ version: 2, page: 0, perPage: 100 })` pin to a past snapshot. Experiments can be pinned to a version too.

## Snapshot artifacts
`createDatasetSnapshot()` and `parseDatasetSnapshot()` from `@mastra/core/datasets` build and validate a versioned JSON artifact (formatVersion 1, datasetIdentity, configuration, items with itemIdentity/createdAt/updatedAt/payload, provenance) with a SHA-256 digest. They are pure format helpers: no storage export/import. Use stable lowercase UUIDs; timestamps are UTC ISO 8601 with milliseconds. Default size budget 4 MiB (`{ maxBytes }` to change); `parseDatasetSnapshot` is the one for untrusted text (budget and duplicate-key rejection). Max nesting depth 100. A matching digest proves integrity, not authorship, and nothing is redacted.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
