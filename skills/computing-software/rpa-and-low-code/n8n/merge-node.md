---
id: computing-software.rpa-and-low-code.n8n.merge-node
name: merge-node
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, merge-node, join, append, sql-query, combine-by]
level: practitioner
status: docs-checked
description: "Use the n8n Merge node: Append, Combine by matching fields, position or all combinations, join-style Output Type, SQL Query mode with parameters and Choose Branch."
sources:
  - https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.merge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: combine data streams after all inputs are available. More than two inputs and **Mode > SQL Query** need n8n 1.49.0 or later.

## Modes
- **Append**: keep everything, items of each input one after another (**Number of Inputs**).
- **Combine** (two inputs), **Combine By**:
  - **Matching Fields**: **Fields to Match**; **Output Type** is Keep Matches (inner join, default), Keep Non-Matches, Keep Everything (outer join), Enrich Input 1 (left join), Enrich Input 2 (right join).
  - **Position**: index 0 with index 0, and so on.
  - **All Possible Combinations**: cross product, merging same-named fields.
  - Options: **Clash Handling**, **Fuzzy Compare** (treat `"3"` and `3` as equal; default off), **Disable Dot Notation**, **Multiple Matches** (all matches or first only), **Include Any Unpaired Items** (position merges leave unpaired items out by default).
- **SQL Query**: inputs are tables `input1`, `input2`, `input3` in order, AlaSQL syntax:
```sql
SELECT * FROM input1 LEFT JOIN input2 ON input1.name = input2.id
```
Use `?` placeholders with **Options > Query Parameters** (comma-separated values or an expression returning an array) so dynamic values are treated as data: `SELECT * FROM input1 WHERE name = ? AND age > ?;` with `{{ [ "Alex", 20 ] }}`.
- **Choose Branch**: wait for both inputs, then output Input 1 data, Input 2 data, or a single empty item.

## Gotchas
- Uneven counts: Input 1 takes precedence. With 5 items in Input 1 and 10 in Input 2, only 5 are processed (position merge).
- **Empty Query Result** option (n8n 1.95.0, Merge node version 3.2): older Merge nodes always output `{ "success": true }` when a query returns no rows; add a new Merge node to get the option (default Empty Result, or Success).
- Example: Combine by Matching Fields on `language` gives each person the right greeting; Append just stacks rows with blank cells.

## Checked
Method: docs-checked 2026-11-09 against the n8n Merge node page (docs.n8n.io, text and Markdown versions, read in full).
Nothing removed; the SQL examples, version notes, Output Type join mappings and the uneven-input behaviour all match the page.
