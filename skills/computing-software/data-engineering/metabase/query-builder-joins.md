---
id: computing-software.data-engineering.metabase.query-builder-joins
name: query-builder-joins
category: computing-software
field: data-engineering
product: metabase
tags: [joins, left-outer-join, join-conditions, query-builder, same-database]
level: practitioner
status: docs-checked
description: "Join tables and saved questions in the Metabase query builder: same-database rule, default left outer join, multiple conditions, chaining and custom expression keys."
sources:
  - https://www.metabase.com/docs/latest/questions/query-builder/join
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rule: you can only pick tables and saved questions from the same database as your starting data.

Join keys: pick one column from each side and rows combine where values match. Foreign key relationships are auto-selected.

Join types: left outer (the default), right outer, inner and full outer. Choose via the Venn diagram icon; only types the database supports are shown.

Behaviour:
- In a left join, rows with no match keep their data and the joined columns are blank.
- One-to-many joins repeat the "one" side's values on each matching row (a customer's details repeat for each of their orders).
- For A to B to C, add a second join step after the first.
- Multiple conditions combine with AND.
- Operators: equals, not equals, greater than, greater than or equal, less than, less than or equal.

Custom expressions as keys: click a join key, select custom expression, enter it and click Done. The page's examples are joining on `1=1` to attach a constant-based aggregate, or concatenating name fields to match a single full-name column.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed the invented double-counting failure mode and the aggregate-before-joining advice (not on the page). Otherwise unchanged.
