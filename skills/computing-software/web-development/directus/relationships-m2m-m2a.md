---
id: computing-software.web-development.directus.relationships-m2m-m2a
name: relationships-m2m-m2a
category: computing-software
field: web-development
product: directus
tags: [relationship-m2m, relationship-m2a, junction-collection, translations-relation]
level: advanced
status: docs-checked
description: "Choose between Many to Many, Many to Any (builder blocks) and Translations relationships in Directus and know what junction collections each creates."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/5.relationships.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Many to Many (M2M)**: an extra *junction collection* stores the primary keys of the two related collections, so any number of items relate both ways. Self-referencing M2M is allowed (related articles, friends list, citations).

**Many to Any (M2A)**: one collection relates to items in any collection (matrix/replicator, "builder"). Directus creates an M2A `Alias` field and a junction collection that also stores the related collection name. Use it for reusable page blocks.

**Translations**: creating a Translations interface creates a translations O2M `Alias` field, a `languages` collection, and a junction collection between your collection and `languages`. The translated text lives in the junction collection. The **Generate Translations** wizard in collection settings builds the whole structure in one step.

## Checked

2026-11-04: confirmed against the Directus docs Relationships page (Many to Many, Many to Any, Translations sections): junction collection contents, self-referencing examples, M2A alias field and stored collection name, translations structure, Generate Translations wizard. Removed the choosing list and verify line, which the page does not state.

Method: documentation only; no commands were run.
