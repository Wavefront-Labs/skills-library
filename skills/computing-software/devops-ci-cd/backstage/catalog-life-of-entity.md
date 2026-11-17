---
id: computing-software.devops-ci-cd.backstage.catalog-life-of-entity
name: catalog-life-of-entity
category: computing-software
field: devops-ci-cd
product: backstage
tags: [entity-lifecycle, ingestion, stitching, backstage]
level: advanced
status: docs-checked
description: "Understand how catalog entities flow through providers, processing and stitching before they appear in the API."
sources:
  - https://backstage.io/docs/features/software-catalog/life-of-an-entity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The catalog is a hub: entities are ingested from authoritative sources, held in a database, processed automatically, then served through an API. The main extension points are:

- Entity providers, which feed raw entity data in.
- Policies, which set baseline rules for the shape of entities.
- Processors, which validate, analyse and mutate raw data into its final form.

The three phases are:

1. Ingestion: entity providers fetch raw data from external sources and seed the database. The database tracks which provider owns each entity, and no two providers may emit the same entity. When a provider signals removal the entity and its auxiliary data are purged immediately (eager deletion).
2. Processing: policies and processors continually treat ingested data, and may emit other raw entities, errors, and relations to other entities.
3. Stitching: everything emitted is assembled into the final output entity.

Errors found during processing are reported back on the entity as status items of type `backstage.io/catalog-processing`, so look there when debugging, and check which provider owns the entity.

## Checked

2026-11-03. Confirmed on the Life of an Entity page: entity providers, policies and processors as the extension points, the ingestion, processing and stitching phases, the rule that no two providers may emit the same entity, eager deletion on provider removal, and final entities. On the descriptor format page: status items of type `backstage.io/catalog-processing` carry processing errors. Removed: the statements that entities are invisible until stitched and that new locations appear with delay, which are inferences rather than page text.

Method: documentation only; no commands were run.
