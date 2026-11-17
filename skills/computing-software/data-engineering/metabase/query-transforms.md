---
id: computing-software.data-engineering.metabase.query-transforms
name: query-transforms
category: computing-software
field: data-engineering
product: metabase
tags: [transforms, query-transforms, incremental, checkpoint-column, merge-key, target-table]
level: advanced
status: docs-checked
description: "Build Metabase query transforms that write result tables back to the database: requirements, target schema, preview behaviour, SQL variable rules and incremental options."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/transforms/query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: on Metabase Cloud the **Basic transforms** add-on is needed, and transforms must be enabled first. The database must support transforms. Create one under **Data Studio, Data transformation** using the query builder, SQL, or a copy of a saved question.

Target table: schema and table name are required; type a new schema name to create it. Writes stay within the same database.

Previewing a query transform in the editor does not write the result back to the database. Tags are used by jobs to schedule transforms.

SQL variables must be optional (`[[ ]]`) or have a default value, because scheduled runs cannot supply values.

Incremental transforms:
- By default each run drops and recreates the target table.
- Incremental mode uses a checkpoint column and filters for values greater than the last checkpoint.
- A merge key updates matching rows instead of appending.
- A lookback window catches late-arriving rows.
- Raw SQL needs a table variable with aliases.

Limitations and gotchas:
- You cannot convert between transform types; create a new transform and delete the old one.
- Converting models is plan-gated (the page shows a plans notice), needs admin rights, and the model's database must support transforms.
- Converted outputs get default permissions, not the model's permissions.
- If the transform run fails during conversion, the model is left unchanged; if only the source swap fails, the transform and output table are kept.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed the unsupported CREATE SCHEMA claim (not on this page), softened the plan claim, and added the conversion failure behaviour. Otherwise unchanged.
