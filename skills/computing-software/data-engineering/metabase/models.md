---
id: computing-software.data-engineering.metabase.models
name: models
category: computing-software
field: data-engineering
product: metabase
tags: [models, model-metadata, search-indexing, version-history, curated-data]
level: practitioner
status: docs-checked
description: "Create and curate Metabase models: from scratch or from a saved question, per-column metadata for SQL models, search indexing limits, overwrite-on-save and phase-out."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/models/models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Creation: build a model from scratch via the Models tab or the command palette, or convert a saved question with **...** then **Turn this into a model**. Query builder models get metadata filled in automatically; SQL models need it set manually. New models are pinned to the current collection.

Per-column metadata: display name and description; database column mapping (SQL models); column type, which lets SQL models be explored in the query builder; table and detail views, or detail views only; display as text or link; search indexing.

Limitations:
- Breaking-change detection is a plan-gated feature (the page shows a plans notice) and only catches broken column references, not type or logic changes.
- Search indexing works only for text fields in records with integer entity keys and indexes at most 25,000 unique values.
- Version history keeps the previous fifteen versions.

Gotchas:
- Saving changes to a model's query overwrites the existing model, unlike questions, which prompt you to save a copy.
- Deleting a model affects questions that use it.
- The page opens with "Consider using Transforms instead of models", says transforms are the successor, and says Metabase will gradually phase models out. Admins can convert models to transforms one at a time; the model then becomes a saved question.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Softened the Pro/Enterprise claim for breaking-change checks (page shows only a plans notice) and added the conversion detail. Otherwise unchanged.
