---
id: computing-software.data-engineering.metabase.custom-expressions
name: custom-expressions
category: computing-software
field: data-engineering
product: metabase
tags: [custom-expressions, custom-column, case, aggregation, query-builder]
level: practitioner
status: docs-checked
description: "Write Metabase custom expressions in the query builder: bracketed column names, double-quoted strings and dates, aggregation placement rules, and Boolean filter requirements."
sources:
  - https://www.metabase.com/docs/latest/questions/query-builder/expressions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Where: create a Custom Column, or choose Custom Expression under Filter or Summarize. Give each expression a name; if Done is grayed out, check the expression is valid and named.

Uses: custom columns (`[Subtotal] / [Quantity]`), filters (`contains([comment], "Metabase")`), summaries (`Share([Total] > 50)`).

Syntax:
- Column references use square brackets, such as `[Subtotal]`; `[ConnectedTableName.Column]` for tables linked by foreign key. Saved metrics and segments are referenced the same way.
- The page's examples write string literals in double quotes: `"CA"`.
- Dates in filter expressions must be `"YYYY-MM-DD"` in double quotes, e.g. `between([Created At], "2020-01-01", "2020-03-31")`.
- Conditionals: `case(condition, result, ..., default)`, alias `if`.
- Operators: `+ - * /`, comparisons `> >= < <= = !=`, `AND`, `OR`, `NOT`, parentheses for grouping. For date math use date functions such as `dateDiff`.

Placement rules:
- Aggregations take values from many rows and can only be used in Summarize. `[Subtotal] + [Tax]` works as a custom column, but `Sum([Subtotal] + [Tax])` does not (it is valid as a custom metric expression in Summarize).
- Functions act on each value in a column (e.g. `contains`, `ceil`).
- A filter expression must return true or false; `[Subtotal] + [Tax]` alone is invalid, `[Subtotal] + [Tax] < 100` is valid.
- Arguments of AND, OR must be Boolean. Functions can be used inside the condition of `CountIf` and `SumIf`.

Tools: an auto-format button and a function browser (toggle the "f" at the right of the editor); a full expression list is on a separate page.

## Checked
Method: 2026-11-08 read the cited Metabase expressions page in full (raw docs source). Removed the unsupported claim that single quotes or unbracketed names fail with only a disabled Done button (the page does not say this); added the connected-table, date-math and CountIf points; other claims confirmed.
