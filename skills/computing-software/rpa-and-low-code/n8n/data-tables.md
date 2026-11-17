---
id: computing-software.rpa-and-low-code.n8n.data-tables
name: data-tables
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, data-tables, storage, csv-import, variables, size-limit]
level: practitioner
status: docs-checked
description: "Use n8n data tables for persistent workflow data: create via UI, Data Table node or API, CSV import and export, the 200 MiB limit and how they differ from variables."
sources:
  - https://docs.n8n.io/build/work-with-data/data-tables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: store and reuse data inside n8n without an external database. Good for persisting data across workflows in a project, de-duplication markers or trigger controls, reusable prompts, evaluation data for AI workflows and lookup tables.

## Three ways to work with them
1. **Data Table node** inside workflows (create, retrieve, update, delete rows).
2. **DataTable API**: the `/datatables` endpoint of the n8n API.
3. **Data tables tab** in a project: split button at top right, **Create Data table**, name it, then **From scratch** (define columns and rows) or **Import CSV** (creates structure and rows). You can rename or delete tables and columns, reorder columns, add/edit/delete rows, and favorite the table. Download a CSV from the three-dot menu, **Download CSV**.

## Limits
- Total storage across all data tables defaults to 200 MiB; self-hosted can change it with `N8N_DATA_TABLES_MAX_SIZE_BYTES`. A warning shows near 80% and at the limit; exceeding it disables manual additions and makes workflow inserts or updates error.
- Tables in a project are visible to all project members; admins and the owner see every user's tables.
- Not accessible from a Code node: built-in methods and variables cannot read data table values.

## Versus variables
Data tables give tabular, structured, project-scoped data. Variables work across projects, display individual values, suit short values and can be used as expressions; they have no row-column structure.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/work-with-data/data-tables

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
