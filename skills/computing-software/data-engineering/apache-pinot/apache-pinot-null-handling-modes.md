---
id: computing-software.data-engineering.apache-pinot.apache-pinot-null-handling-modes
name: apache-pinot-null-handling-modes
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, null-handling, enablenullhandling, nullhandlingenabled, enablecolumnbasednullhandling, is-not-null, null-backfill, indexes-null]
level: practitioner
status: docs-checked
description: "Pinot null semantics: off by default so IS NOT NULL is always true, basic vs advanced modes, config switches, lossy null backfill."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/null-value-support.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null handling modes

By default null handling is **disabled**: a missing value is replaced by the column default, so `IS NOT NULL` is always true.

Two levels:
- **Basic**: nulls are recorded at ingestion (a null vector index) so they can be filtered.
- **Advanced**: at query time `SET enableNullHandling=true;` makes functions and aggregations treat nulls with SQL semantics.

Switches:
- Per-column (recommended, and the only way the multi-stage engine supports nulls): `enableColumnBasedNullHandling` in the schema, with a `notNull` field spec per column.
- Table-wide `tableIndexConfig.nullHandlingEnabled` (deprecated since 1.1.0). Column-based storing wins if both are set.

Adding nulls to existing segments:
```
{ "name": "amount", "indexes": { "null": { "backfill": true } } }
```
in `fieldConfigList`, then reload. This is **lossy**: only values equal to the column default can be identified as null, so a real value equal to the default (for example 0) may be marked null.

## Checked

2026-11-09: confirmed against the Pinot Null value support page (pinot-docs build-with-pinot/querying-and-sql/null-value-support.md): disabled by default, the disabled/basic/advanced behaviour table, null vector index at ingestion, `enableNullHandling` query option, column-based versus table-based storing, and the `indexes.null.backfill` option with its lossy reload. Removed the unconfirmed claims about partial upsert and star-tree needing their own `nullHandlingEnabled` flag.

Method: documentation only; no commands were run.
