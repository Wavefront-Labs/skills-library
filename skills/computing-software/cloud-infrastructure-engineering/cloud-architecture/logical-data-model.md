---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.logical-data-model
name: logical-data-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, logical-data-model, togaf, phase-c, data-entity-catalogue, data-architecture]
level: practitioner
status: draft
description: "Produce a logical data model and data entity catalogue in TOGAF Phase C: entities, attributes, keys, ownership, systems of record and data lifecycle per entity."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap05.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://www.dama.org/cpages/body-of-knowledge"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logical data model and data entity catalogue

## Steps
1. **Start from the conceptual model** (Phase B information map); decompose concepts into
   entities with attributes, primary/natural keys and relationships, normalised to about 3NF.
   Technology-neutral: no column types or table partitioning yet.
2. **Data entity / data component catalogue**: each entity with business owner, steward,
   classification, system of record, systems holding copies, retention, quality rules.
3. **Data entity / business function matrix** and **application / data matrix**: which
   function and application create, read, update, delete each entity.
4. **Lifecycle**: creation, archival and deletion triggers per entity; this drives storage
   tiering and erasure design in the cloud.
5. **Identify integration needs**: every entity copied across applications needs a sync
   mechanism (CDC, events, API) recorded in the interface catalogue.
6. **Review with data owners** and version it in the architecture repository.

## Gotchas
- Logical models drawn from one application's schema bake in its quirks.
- Copies without a declared system of record cause reconciliation incidents after migration.

## Verify
- [ ] Every entity has owner, system of record and classification.
- [ ] Application/data CRUD matrix complete for in-scope apps.
