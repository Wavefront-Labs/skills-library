---
id: computing-software.data-engineering.metabase.segments
name: segments
category: computing-software
field: data-engineering
product: metabase
tags: [segments, saved-filters, data-studio, semantic-layer, remote-sync]
level: intro
status: docs-checked
description: "Create Metabase segments as saved table filters in Data Studio, see where they appear in the query builder, and know their primary-table-only limitation and sync caveats."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/semantic-layer/segments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Segments are saved filters on tables. Create one in Data Studio under Connected data, on the table's Segments tab (**+ New Segment**): add filters (for example Active = true), name the segment, optionally preview its records, and save. For now, segments can also be managed through Admin, Table Metadata (the page links this as "legacy segments").

Usage: segments appear in the Filter block of the query builder; selecting one applies its filters.

Limitations:
- Segments work only in the query builder, not as reusable SQL. Snippets cover that case.
- They apply only when the segment's table is the primary data source. They do not appear in joins, or in questions and models built on that table.
- Anyone who is an admin or in the Data Analysts group can create segments on tables they can query. No other access controls exist.

Gotchas:
- Deleting a segment does not break existing questions; they keep the filters they already use.
- Under Remote Sync, only segments on published Library tables sync to Git.
- In read-only remote sync mode you cannot create segments on published tables.

Permissions: creating, editing or deleting a segment needs admin or Data Analysts membership plus Create queries permission on the table; using one needs Create queries permission on the table.

The page's use case is an official definition of a subset, such as what counts as an "active user".

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Replaced the inferred "use a metric when aggregate" advice with the page's own use case and added the permissions section. Otherwise unchanged.
