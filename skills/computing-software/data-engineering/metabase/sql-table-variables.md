---
id: computing-software.data-engineering.metabase.sql-table-variables
name: sql-table-variables
category: computing-software
field: data-engineering
product: metabase
tags: [table-variable, emit-table-alias, sql-snippets, native-query, sql-variables]
level: practitioner
status: docs-checked
description: "Use Metabase table variables in SQL FROM and JOIN clauses, set Table to map to, choose Emit table alias, and plan around the dashboard and transform limitations."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/table-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: write `{{variable}}` wherever a table name goes, including `FROM` and `JOIN`, for example `FROM {{table}} AS t`.

Setup: in the Variables sidebar change the variable type to **Table**, then pick a table under **Table to map to**. That field is required.

**Emit table alias**:
- On: you reference the variable by its name, such as `var_name.id`.
- Off: you add your own alias, such as `{{var_name}} as o`.

The eye icon previews the SQL Metabase will run.

Snippets: put `{{table}}` inside a snippet, insert the snippet with `{{snippet: name}}`, and map the table separately in each question that uses it. This is the way to share one SQL body across several tables of the same shape.

Limitations:
- Cannot be connected to dashboard filter widgets; each question must set its table directly.
- Native SQL only, not the query builder.
- No input widget exists for users to choose a table.
- Not yet supported in transforms.

Clicking the eye icon is the page's way to see the exact code Metabase will run.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed an invented failure-mode line (the page only says the mapping is required). Rest unchanged.
