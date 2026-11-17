---
id: computing-software.data-engineering.metabase.sql-field-filters
name: sql-field-filters
category: computing-software
field: data-engineering
product: metabase
tags: [field-filter, sql-variables, table-and-field-alias, widgets, native-query]
level: practitioner
status: docs-checked
description: "Use Metabase field filter variables in SQL: bare WHERE syntax, mapping a field, aliases for tables and CTEs, join requirements, quoting rules and the custom column limit."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/field-filters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: write the variable alone in the WHERE clause, for example `WHERE {{state}}`, with no column or operator. Metabase interpolates the SQL itself, which is how multi-value selections and date ranges work.

MongoDB: place it in a `$match` clause, for example `[ {$match: {{date_var}} } ]`.

Setup: open the variables side panel, set **Variable type** to "Field filter", then choose a **Field to map to**.

Aliases:
- If the table is aliased (`products AS p`), enter the alias in **Table and field alias**, such as `p.category`.
- For CTEs use the CTE name, such as `expensive_products.category`.

Joins: the main query must include every table the filter points to, otherwise you get a SQL syntax error.

Quoting: in BigQuery quote schemas and tables with backticks; in Oracle use double quotes.

Limitation: field filters map only to database fields. For custom columns, use a basic variable.

To make a filter optional, see the optional variables page, using the form `[[AND {{category}}]]`.

## Checked
2026-11-03. Confirmed against the Metabase docs page Questions, Native editor, Field filters: bare WHERE syntax, MongoDB $match form, variable type and Field to map to, Table and field alias for aliases and CTEs, join requirement and syntax error, BigQuery backticks and Oracle double quotes, basic-variable fallback for custom columns. Removed the unsupported failure-mode diagnosis.
Method: documentation only; no commands were run.
