---
id: computing-software.rpa-and-low-code.uipath.uipath-datatable-operations
name: uipath-datatable-operations
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-data-tables-excel, uipath-datatable-operations]
level: practitioner
status: draft
description: "Filter, join, sort and build tables."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manipulate data tables
**Goal:** Filter, join, sort and build tables.

- Build Data Table, Filter Data Table, Join Data Tables, Sort, Remove Duplicate Rows, Lookup Data Table and Merge activities; or LINQ in expressions.
- Use Output Data Table to inspect.
- Avoid per-row Excel writes in loops; batch with Write Range.

## Gotchas
- Column types change in Excel reads (everything may be string); convert explicitly.

## Self-check
Row counts match expected after each transformation.
