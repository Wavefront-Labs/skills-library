---
id: computing-software.data-engineering.metabase.sql-basic-variables
name: sql-basic-variables
category: computing-software
field: data-engineering
product: metabase
tags: [sql-variables, basic-variables, double-braces, native-query, in-clause]
level: intro
status: docs-checked
description: "Add basic variables to Metabase SQL questions with double braces, choose Text, Number, Date or Boolean types, handle multiple values, and know when to use field filters."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/basic-sql-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap a variable name in double braces: `{{variable_name}}`.

A basic variable includes its own operator: `category = {{category_filter}}`. A field filter, by contrast, is written alone: `WHERE {{category}}`. The variable is not connected to a database field; the value set in the widget is simply inserted, so entering `Gizmo` produces `category = 'Gizmo'`.

MongoDB native queries define the variable inside the match clause: `[{ $match: { category: {{category}} } }]`.

Variable types (basic variables offer limited filter types):
- Text and Number: a plain input box.
- Date: a simple date picker.
- Boolean: a "this or that" picker.
- For a more expressive widget, such as a dynamic date picker, use a field filter variable instead.

Multiple values: write the SQL so several values make sense when interpolated, for example `WHERE category IN ({{category_vars}})`, then set **People can pick** to multiple values. The page adds that you are probably better off with a field filter here.

Gotchas:
- To filter on a database field, the page says to prefer a field filter variable, which uses different syntax.
- To make a variable optional, see the optional variables skill.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed two unsupported claims (dashboard single-value restriction; loss of dropdown values). Rest unchanged.
